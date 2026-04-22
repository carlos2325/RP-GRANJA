#!/usr/bin/env python3
"""
Control GPIO - Relés, LED, Bombas
Compatible con Python 3.13 + gpiozero
"""

from gpiozero import OutputDevice
import time
from datetime import datetime

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
        self.device = OutputDevice(pin, initial_value=False)

    def activar(self):
        """Encender dispositivo"""
        self.device.on()
        self.estado = True
        self._log("ACTIVADO")

    def desactivar(self):
        """Apagar dispositivo"""
        self.device.off()
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
        print(f"Zona {zona} no existe")
        return

    print(f"Iniciando riego Zona {zona} ({duracion}s)...")
    device.activar()
    time.sleep(duracion)
    device.desactivar()
    print(f"Riego Zona {zona} completado")

if __name__ == '__main__':
    try:
        riego_automatico(zona=1, duracion=10)
    except KeyboardInterrupt:
        print("\nInterrumpido por usuario")
