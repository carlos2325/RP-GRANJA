#!/usr/bin/env python3
"""
Lector DHT22 - Temperatura y Humedad
Optimizado para Raspberry Pi
"""

import Adafruit_DHT
import time
from datetime import datetime

# Pin GPIO donde está conectado el DHT22
DHT_PIN = 17
DHT_SENSOR = Adafruit_DHT.DHT22

def leer_dht22(intentos=3):
    """
    Leer DHT22 con reintentos
    Retorna: (humedad, temperatura) o (None, None) si falla
    """
    for intento in range(intentos):
        humedad, temperatura = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

        if humedad is not None and temperatura is not None:
            return humedad, temperatura

        time.sleep(1)

    return None, None

def log_lectura(humedad, temperatura):
    """Loguear lectura con timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if humedad and temperatura:
        print(f"[{timestamp}] ✅ Temp: {temperatura:.1f}°C | Humedad: {humedad:.1f}%")
        return True
    else:
        print(f"[{timestamp}] ❌ Error leyendo DHT22")
        return False

if __name__ == '__main__':
    print("🌡️  Iniciando lectura DHT22...")

    try:
        while True:
            humedad, temperatura = leer_dht22()
            log_lectura(humedad, temperatura)
            time.sleep(30)  # Leer cada 30 segundos

    except KeyboardInterrupt:
        print("\n❌ Detenido por usuario")
