"""
Configuración del proyecto Granja IoT
"""

import os

_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
if os.path.isfile(_env_path):
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, value = line.partition('=')
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'cambiar-en-produccion-clave-segura')

# ==================== SENSORES ====================
SENSORES = {
    'DHT22': {
        'pin': 17,
        'tipo': 'temperatura_humedad',
        'intervalo': 30  # segundos
    },
    'HUMEDAD_SUELO': {
        'pin': 27,
        'tipo': 'humedad_suelo',
        'intervalo': 60
    },
    'LUZ': {
        'pin': 22,
        'tipo': 'luz',
        'intervalo': 120
    }
}

# ==================== DISPOSITIVOS ====================
DISPOSITIVOS = {
    'RIEGO_1': {
        'pin': 18,
        'tipo': 'riego',
        'nombre': 'Riego Zona 1'
    },
    'RIEGO_2': {
        'pin': 23,
        'tipo': 'riego',
        'nombre': 'Riego Zona 2'
    },
    'LUZ_LED': {
        'pin': 24,
        'tipo': 'luz',
        'nombre': 'Luz LED'
    }
}

# ==================== MQTT ====================
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPICS = {
    'sensores': 'granja/sensores/#',
    'dispositivos': 'granja/dispositivos/#'
}

# ==================== FLASK ====================
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = False

# ==================== BASE DE DATOS ====================
DB_PATH = 'granja.db'
DB_RETENTION_DAYS = 7  # Limpiar datos más viejos
