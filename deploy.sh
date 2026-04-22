#!/bin/bash
# Deploy script para Raspberry Pi - Granja IoT

set -e

echo "🚀 Iniciando deploy en Raspberry Pi..."

# Variables
DEST="/home/pi/granja-iot"
VENV_PATH="/home/pi/granja-venv"

# 1. Crear directorio
echo "📁 Creando directorio..."
mkdir -p $DEST

# 2. Copiar archivos
echo "📋 Copiando archivos..."
cp -r app.py config.py requirements.txt templates sensors $DEST/

# 3. Crear venv
echo "🐍 Creando venv Python..."
python3 -m venv $VENV_PATH
source $VENV_PATH/bin/activate

# 4. Instalar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r $DEST/requirements.txt

# 5. Crear base de datos
echo "🗄️  Inicializando BD..."
cd $DEST
python3 -c "from app import init_db; init_db()"

# 6. Test simple
echo "✅ Test de conexión..."
python3 -c "import flask; print(f'Flask OK')"

echo ""
echo "✅ Deploy completado!"
echo ""
echo "Para ejecutar:"
echo "  source $VENV_PATH/bin/activate"
echo "  cd $DEST"
echo "  python3 app.py"
