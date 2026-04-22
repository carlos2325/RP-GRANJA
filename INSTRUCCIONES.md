# 🌾 Granja IoT - Instrucciones Finales

## ESTADO ACTUAL
✅ Proyecto 100% preparado  
❌ SSH en Raspberry: Pendiente solucionar

## PRÓXIMOS PASOS CUANDO SSH FUNCIONE

### 1. Conectarse a Raspberry
```bash
ssh pi@192.168.1.135
# Contraseña: raspberry
```

### 2. Copiar proyecto
```bash
cd ~
git clone <URL-REPO> granja-iot
cd granja-iot
```

O copiar archivos manualmente:
```bash
scp -r /Volumes/HD\ MAC\ BASE/Projects/RP-GRANJA/* pi@192.168.1.135:~/granja-iot/
```

### 3. Instalar
```bash
python3 -m venv venv
source venv/bin/activate
pip install Flask==2.3.2
```

### 4. Ejecutar TEST (Hola Mundo)
```bash
python3 app_simple.py
```

Luego acceder a: **http://192.168.1.135:5000**

### 5. Ejecutar PRODUCCIÓN (Full)
```bash
python3 app.py
```

## ARCHIVOS DISPONIBLES

- **app_simple.py** → Hola Mundo (test rápido)
- **app.py** → Sistema completo con BD + API
- **templates/dashboard.html** → UI con HTMX
- **sensors/** → Scripts para DHT22, GPIO, MQTT
- **config.py** → Configuración centralizada

## ALTERNATIVAS SI SSH NO FUNCIONA

1. **Re-grabar con Raspberry Pi OS Desktop (Full)**
   - Tendrás interfaz gráfica
   - Puedes abrir terminal local

2. **Usar otra Raspberry Pi**
   - Si tienes disponible

3. **Acceso por USB-Serial (UART)**
   - Requiere adaptador USB-UART
   - Conectar a GPIO

## SOPORTE

Todo el código está optimizado para:
- Raspberry Pi con 512MB RAM
- Python 3.7+
- Ethernet (no WiFi)
- Flask + HTMX (sin frameworks pesados)

