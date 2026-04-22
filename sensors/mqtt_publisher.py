#!/usr/bin/env python3
"""
MQTT Publisher - Publicar sensores a broker MQTT
Ideal para sistemas con múltiples nodos
"""

import paho.mqtt.client as mqtt
import Adafruit_DHT
import time
import json
from datetime import datetime

# Configuración MQTT
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_SENSORES = 'granja/sensores/'

# Configuración sensores
DHT_PIN = 17
DHT_SENSOR = Adafruit_DHT.DHT22

# Cliente MQTT
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    """Callback cuando se conecta al broker"""
    if rc == 0:
        print("✅ Conectado a MQTT broker")
    else:
        print(f"❌ Error de conexión MQTT: {rc}")

def on_disconnect(client, userdata, rc):
    """Callback cuando se desconecta"""
    print(f"⚠️  Desconectado de MQTT: {rc}")

def conectar_mqtt():
    """Conectar a broker MQTT"""
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.loop_start()
        return True
    except Exception as e:
        print(f"❌ No se pudo conectar a MQTT: {e}")
        return False

def leer_dht22():
    """Leer DHT22 con manejo de errores"""
    humedad, temperatura = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return humedad, temperatura

def publicar_sensor(tipo, valor):
    """Publicar sensor a MQTT"""
    topic = f"{MQTT_TOPIC_SENSORES}{tipo}"
    payload = json.dumps({
        'valor': valor,
        'timestamp': datetime.now().isoformat(),
        'dispositivo': 'raspberry-granja-01'
    })

    try:
        client.publish(topic, payload, qos=1)
        print(f"📤 Publicado: {topic} = {valor}")
    except Exception as e:
        print(f"❌ Error publicando {topic}: {e}")

if __name__ == '__main__':
    print("🌡️  MQTT Publisher iniciado...")

    if not conectar_mqtt():
        print("❌ No se pudo conectar. ¿Está corriendo Mosquitto?")
        exit(1)

    try:
        while True:
            humedad, temperatura = leer_dht22()

            if humedad and temperatura:
                publicar_sensor('temperatura', temperatura)
                publicar_sensor('humedad_aire', humedad)
                print(f"✅ Lectura: {temperatura:.1f}°C | {humedad:.1f}%\n")
            else:
                print("❌ Error leyendo DHT22\n")

            time.sleep(30)  # Publicar cada 30 segundos

    except KeyboardInterrupt:
        print("\n❌ Detenido por usuario")
    finally:
        client.loop_stop()
        client.disconnect()
