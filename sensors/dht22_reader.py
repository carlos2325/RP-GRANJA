#!/usr/bin/env python3
"""
Lector DHT22 - Temperatura y Humedad
Compatible con Python 3.13 + adafruit-circuitpython-dht
"""

import board
import adafruit_dht
import time
from datetime import datetime

# Pin GPIO donde está conectado el DHT22
DHT_PIN = board.D17
dht_device = adafruit_dht.DHT22(DHT_PIN)

def leer_dht22(intentos=3):
    """
    Leer DHT22 con reintentos
    Retorna: (humedad, temperatura) o (None, None) si falla
    """
    for intento in range(intentos):
        try:
            temperatura = dht_device.temperature
            humedad = dht_device.humidity
            if humedad is not None and temperatura is not None:
                return humedad, temperatura
        except RuntimeError:
            pass
        time.sleep(2)

    return None, None

def log_lectura(humedad, temperatura):
    """Loguear lectura con timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if humedad and temperatura:
        print(f"[{timestamp}] Temp: {temperatura:.1f}C | Humedad: {humedad:.1f}%")
        return True
    else:
        print(f"[{timestamp}] Error leyendo DHT22")
        return False

if __name__ == '__main__':
    print("Iniciando lectura DHT22...")

    try:
        while True:
            humedad, temperatura = leer_dht22()
            log_lectura(humedad, temperatura)
            time.sleep(30)

    except KeyboardInterrupt:
        print("\nDetenido por usuario")
    finally:
        dht_device.exit()
