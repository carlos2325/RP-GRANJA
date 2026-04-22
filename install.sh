#!/bin/bash
# Script de instalación automática para Granja IoT
# Ejecutar: bash install.sh

set -e

echo "🌾 Instalando Granja IoT..."
echo ""

# 1. Update system
echo "📦 Actualizando sistema..."
sudo apt update
sudo apt upgrade -y

# 2. Install Python
echo "🐍 Instalando Python..."
sudo apt install -y python3 python3-pip python3-venv python3-dev

# 3. Create project directory
echo "📁 Creando directorio..."
mkdir -p ~/granja-iot
cd ~/granja-iot

# 4. Copy files (if not already there)
if [ ! -f "app.py" ]; then
    echo "📋 Descargando proyecto..."
    # Aquí iría git clone o scp
    echo "⚠️  Copia los archivos manualmente"
    exit 1
fi

# 5. Create venv
echo "🔧 Creando venv..."
python3 -m venv venv
source venv/bin/activate

# 6. Install dependencies
echo "📚 Instalando dependencias..."
pip install --upgrade pip
pip install Flask==2.3.2

# 7. Create database
echo "🗄️  Inicializando BD..."
python3 -c "from app import init_db; init_db()" || echo "⚠️  app.py no encontrado"

# 8. Test
echo "✅ Test de instalación..."
python3 -c "import flask; print(f'Flask {flask.__version__} OK')"

echo ""
echo "✅ ¡Instalación completada!"
echo ""
echo "Para ejecutar:"
echo "  cd ~/granja-iot"
echo "  source venv/bin/activate"
echo "  python3 app_simple.py"
echo ""
echo "Acceso: http://192.168.1.135:5000"
