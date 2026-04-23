# Cableado (Hardware)

Este documento describe el cableado físico (GPIO/BCM → pin físico) para la Raspberry Pi y cómo conectar sensores/actuadores definidos en `config.py`.

## Convenciones

- `GPIO/BCM`: número de GPIO usado en software (lo que aparece en `config.py`).
- `Pin físico`: número del header de 40 pines (lo que aparece en la vista **Hardware**).
- Alimentación:
  - 3.3V: pines físicos 1 y 17
  - 5V: pines físicos 2 y 4
  - GND: pines físicos 6, 9, 14, 20, 25, 30, 34, 39

## Checklist de conexión

- Verifica que el tipo de señal del sensor sea compatible con 3.3V.
- Comparte GND entre Raspberry y todos los módulos.
- Evita alimentar módulos de 3.3V desde 5V.

## Pines reservados / buses

- I2C:
  - SDA: pin físico 3 (GPIO2)
  - SCL: pin físico 5 (GPIO3)

## Sensores y actuadores

La fuente de verdad es `config.py`. La vista **Hardware** muestra:

- Qué GPIO/BCM usa cada sensor/actuador
- Qué pin físico corresponde
- Qué pines quedan marcados como “EN USO”
