# 🌾 Granja IoT - Raspberry Pi

Sistema IoT para monitoreo y control de granjas.

## Stack
- **Backend:** Python + Flask
- **Frontend:** HTMX + HTML/CSS vanilla
- **BD:** SQLite
- **Comunicación:** MQTT (Mosquitto)

## Especificaciones
- Raspberry Pi 512MB
- Ethernet (conectada)
- WiFi (problemas)

## Estructura
```
granja-iot/
├── app.py              # Flask main
├── sensors/            # Scripts de sensores
├── templates/          # HTML
├── static/             # CSS/JS
├── requirements.txt    # Dependencias Python
└── config.py           # Configuración
```

## Setup
1. **SSH a Raspberry:** `ssh pi@192.168.1.135` — Ver **[SSH.md](SSH.md)** para la guía completa de conexión.
2. Install Python deps: `pip install -r requirements.txt`
3. Run: `python app.py`
4. Access: `http://192.168.1.135:5000`
