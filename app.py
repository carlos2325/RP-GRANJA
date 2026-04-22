#!/usr/bin/env python3
"""
🌾 Granja IoT - Flask Backend
Optimizado para Raspberry Pi 512MB
"""

from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import os
import html
from datetime import datetime

try:
    from config import SECRET_KEY
except Exception:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'cambiar-en-produccion')

try:
    from config import SENSORES, DISPOSITIVOS
except Exception:
    SENSORES = {}
    DISPOSITIVOS = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = False

# ==================== DATABASE ====================
DB_PATH = 'granja.db'

def init_db():
    """Inicializar base de datos SQLite"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS sensores (
        id INTEGER PRIMARY KEY,
        tipo TEXT,
        valor REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS dispositivos (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        tipo TEXT,
        estado INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('SELECT COUNT(*) FROM dispositivos')
    if c.fetchone()[0] == 0:
        c.executemany('INSERT INTO dispositivos (nombre, tipo, estado) VALUES (?, ?, ?)', [
            ('Bomba de Agua (Sur)', 'actuador', 0),
            ('Luces Infrarrojas (Cerditos)', 'actuador', 0),
            ('Ventilador Extractor', 'actuador', 0)
        ])

    conn.commit()
    conn.close()

def get_db():
    """Obtener conexión a BD"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ==================== SENSORES ====================
def leer_sensores():
    """Leer todos los sensores (DHT22, humedad suelo, etc)"""
    # TODO: Integrar con sensores reales via GPIO
    datos = {
        'temperatura': 24.5,
        'humedad_aire': 65,
        'humedad_suelo': 45,
        'luz': 800
    }
    return datos

def guardar_sensor(tipo, valor):
    """Guardar lectura de sensor en BD"""
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO sensores (tipo, valor) VALUES (?, ?)', (tipo, valor))
    conn.commit()
    conn.close()

def tarea_lectura_sensores():
    """Tarea periódica: leer sensores cada 30s"""
    datos = leer_sensores()
    for tipo, valor in datos.items():
        guardar_sensor(tipo, valor)

# ==================== RUTAS ====================
@app.route('/')
def index():
    """Dashboard principal"""
    return render_template('dashboard.html')

@app.route('/hardware')
def hardware():
    return render_template('hardware.html', sensores=SENSORES, dispositivos=DISPOSITIVOS)

@app.route('/api')
def api_page():
    return render_template('api.html')

@app.route('/docs')
def docs():
    items = [
        {'key': 'README.md', 'label': 'README.md'},
        {'key': 'INSTRUCCIONES.md', 'label': 'INSTRUCCIONES.md'},
        {'key': 'DEPLOY.md', 'label': 'DEPLOY.md'},
        {'key': 'SSH.md', 'label': 'SSH.md'},
        {'key': 'config.py', 'label': 'config.py'},
        {'key': 'requirements.txt', 'label': 'requirements.txt'},
    ]
    allow = {i['key']: i['label'] for i in items}
    key = request.args.get('file') or 'README.md'
    label = allow.get(key)
    if not label:
        key = 'README.md'
        label = allow[key]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, key)
    content = ''
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception:
        content = 'No se pudo leer el archivo.'
    return render_template('docs.html', items=items, current_label=label, content=html.escape(content))

@app.route('/pages')
def pages():
    rules = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint == 'static':
            continue
        methods = sorted((rule.methods or set()) - {'HEAD', 'OPTIONS'})
        rules.append({
            'rule': rule.rule,
            'endpoint': rule.endpoint,
            'methods': methods,
        })

    def sort_key(r):
        return (0 if r['rule'] == '/' else 1, r['rule'])

    ui_routes = sorted(
        [r for r in rules if not (r['rule'].startswith('/api') or r['rule'] == '/salud')],
        key=sort_key,
    )
    api_routes = sorted(
        [r for r in rules if (r['rule'].startswith('/api') or r['rule'] == '/salud')],
        key=lambda r: r['rule'],
    )
    return render_template('pages.html', ui_routes=ui_routes, api_routes=api_routes)

@app.route('/api/sensores')
def api_sensores():
    """API: obtener historial HTML"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT tipo, valor, timestamp FROM sensores ORDER BY timestamp DESC LIMIT 5''')
    datos = [dict(row) for row in c.fetchall()]
    conn.close()
    html = ""
    for d in datos:
        html += f"""<div style="font-size: 0.9em; padding: 5px; border-bottom: 1px solid #fecfef;">
            <strong>{d['tipo'].title()}:</strong> <span style="color:#e91e63">{d['valor']}</span> 
            <span class="timestamp" style="font-size:0.8em; float:right">({d['timestamp'][11:16]})</span>
        </div>"""
    return html or "<div style='text-align:center; color:#999'>Sin historial. Esperando lecturas...</div>"

@app.route('/api/sensores/ultima')
def api_sensores_ultima():
    """API: última lectura de sensores en HTML"""
    sensores = leer_sensores()
    html = ""
    nombres = {'temperatura': 'Temperatura (°C)', 'humedad_aire': 'Humedad Aire (%)', 'humedad_suelo': 'Humedad Suelo (%)', 'luz': 'Luminosidad'}
    for key, val in sensores.items():
        html += f"""
        <div class="sensor-item">
            <span class="sensor-label">{nombres.get(key, key)}</span>
            <span class="sensor-valor">{val}</span>
        </div>"""
    return html

@app.route('/api/dispositivos')
def api_dispositivos():
    """API: estado de dispositivos en HTML"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM dispositivos')
    datos = c.fetchall()
    conn.close()
    html = ""
    for d in datos:
        estado_badge = '<span class="status-badge status-on" style="background:#d1fae5; color:#065f46;">ON</span>' if d['estado'] else '<span class="status-badge status-off" style="background:#fee2e2; color:#7f1d1d;">OFF</span>'
        btn_class = 'btn-off' if d['estado'] else 'btn-on'
        btn_txt = 'Apagar' if d['estado'] else 'Encender'
        html += f"""
        <div class="device-control">
            <span class="device-name">{d['nombre']} {estado_badge}</span>
            <button hx-post="/api/dispositivos/{d['id']}/toggle" hx-target="#dispositivos-container" class="{btn_class}">{btn_txt}</button>
        </div>"""
    return html

@app.route('/api/dispositivos/<int:device_id>/toggle', methods=['POST'])
def api_toggle_dispositivo(device_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT estado FROM dispositivos WHERE id = ?', (device_id,))
    req = c.fetchone()
    if req:
        nuevo_estado = 0 if req[0] else 1
        c.execute('UPDATE dispositivos SET estado = ? WHERE id = ?', (nuevo_estado, device_id))
        conn.commit()
    conn.close()
    return api_dispositivos()

@app.route('/salud')
def salud():
    """Health check"""
    return '<span class="status-badge status-on" style="background:#d1fae5; color:#065f46;">✅ Sistema en línea</span>'

# ==================== SCHEDULER ====================
scheduler = BackgroundScheduler()
scheduler.add_job(tarea_lectura_sensores, 'interval', seconds=30)

# ==================== MAIN ====================
if __name__ == '__main__':
    init_db()
    scheduler.start()
    # Usar 0.0.0.0 para que sea accesible desde la red
    app.run(host='0.0.0.0', port=5000, threaded=True)
