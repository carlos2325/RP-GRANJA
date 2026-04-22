#!/usr/bin/env python3
"""
Control GPIO - Relés, LED, Bombas
Optimizado para Raspberry Pi con 512MB
"""

import RPi.GPIO as GPIO
import time
from datetime import datetime

# Usar numeración BCM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Configuración de pines
PINES = {
    'riego_1': 18,
    'riego_2': 23,
    'luz_led': 24,
    'bomba_agua': 25
}

class DispositivoGPIO:
    def __init__(self, nombre, pin):
        self.nombre = nombre
        self.pin = pin
        self.estado = False
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def activar(self):
        """Encender dispositivo"""
        GPIO.output(self.pin, GPIO.HIGH)
        self.estado = True
        self._log("ACTIVADO")

    def desactivar(self):
        """Apagar dispositivo"""
        GPIO.output(self.pin, GPIO.LOW)
        self.estado = False
        self._log("DESACTIVADO")

    def toggle(self):
        """Cambiar estado"""
        if self.estado:
            self.desactivar()
        else:
            self.activar()

    def _log(self, accion):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {self.nombre}: {accion}")

# Instanciar dispositivos
dispositivos = {
    nombre: DispositivoGPIO(nombre, pin)
    for nombre, pin in PINES.items()
}

def riego_automatico(zona, duracion=30):
    """
    Activar riego en una zona por X segundos
    """
    device = dispositivos.get(f'riego_{zona}')
    if not device:
        print(f"❌ Zona {zona} no existe")
        return

    print(f"💧 Iniciando riego Zona {zona} ({duracion}s)...")
    device.activar()
    time.sleep(duracion)
    device.desactivar()
    print(f"✅ Riego Zona {zona} completado")

def cleanup():
    """Limpiar GPIO al salir"""
    print("\n🔴 Limpiando GPIO...")
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        # Ejemplo: riego zona 1 durante 10 segundos
        riego_automatico(zona=1, duracion=10)

    except KeyboardInterrupt:
        print("\n❌ Interrumpido por usuario")
    finally:
        cleanup()
