#!/usr/bin/env python3
"""
🌾 Granja IoT - Flask Backend
Optimizado para Raspberry Pi 512MB
"""

from flask import Flask, render_template, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import json
import os
from datetime import datetime

app = Flask(__name__)
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

@app.route('/api/sensores')
def api_sensores():
    """API: obtener últimas lecturas de sensores"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT tipo, valor, timestamp
                 FROM sensores
                 ORDER BY timestamp DESC
                 LIMIT 10''')
    datos = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(datos)

@app.route('/api/sensores/ultima')
def api_sensores_ultima():
    """API: última lectura de cada sensor"""
    sensores = leer_sensores()
    return jsonify(sensores)

@app.route('/api/dispositivos')
def api_dispositivos():
    """API: obtener estado de dispositivos"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM dispositivos')
    datos = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(datos)

@app.route('/api/dispositivos/<int:device_id>', methods=['POST'])
def api_toggle_dispositivo(device_id):
    """API: activar/desactivar dispositivo"""
    nuevo_estado = request.json.get('estado')
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE dispositivos SET estado = ? WHERE id = ?',
              (nuevo_estado, device_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/salud')
def salud():
    """Health check"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

# ==================== SCHEDULER ====================
scheduler = BackgroundScheduler()
scheduler.add_job(tarea_lectura_sensores, 'interval', seconds=30)

# ==================== MAIN ====================
if __name__ == '__main__':
    init_db()
    scheduler.start()
    # Usar 0.0.0.0 para que sea accesible desde la red
    app.run(host='0.0.0.0', port=5000, threaded=True)
