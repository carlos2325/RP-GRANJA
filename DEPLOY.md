# 🌾 Granja IoT - Guía de Deploy

## Estado Actual
- ✅ Proyecto estructurado (Python + Flask + HTMX)
- ✅ Código listo para Raspberry Pi 512MB
- ⏳ SSH en Raspberry: PENDIENTE

## Paso 1: Conectar a Raspberry

```bash
ssh pi@192.168.1.135
# Contraseña: raspberry
```

## Paso 2: Copiar proyecto

```bash
# Desde tu Mac, copiar archivos a Raspberry
scp -r /Volumes/HD\ MAC\ BASE/Projects/RP-GRANJA/* pi@192.168.1.135:~/granja-iot/
```

## Paso 3: Instalar y ejecutar

```bash
ssh pi@192.168.1.135
cd ~/granja-iot

# Crear venv
python3 -m venv venv
source venv/bin/activate

# Instalar
pip install Flask==2.3.2

# Correr
python3 app_simple.py
```

## Acceso

- URL: http://192.168.1.135:5000
- Status: http://192.168.1.135:5000/api/status

---

**PRÓXIMOS PASOS:**
1. Arreglar SSH en Raspberry
2. Deploy del proyecto
3. Test "Hola Mundo"
4. Integración de sensores
