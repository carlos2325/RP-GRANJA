#!/bin/bash
# Setup rápido - Solo Hola Mundo

echo "🚀 Setup Granja IoT - Hola Mundo"

# Update system
sudo apt update
sudo apt install -y python3-pip python3-venv

# Create venv
python3 -m venv ~/granja-venv
source ~/granja-venv/bin/activate

# Install only Flask
pip install Flask==2.3.2

# Create app directory
mkdir -p ~/granja-iot
cd ~/granja-iot

# Test Flask
python3 << 'PYTHON'
import flask
print(f"✅ Flask {flask.__version__} instalado")
PYTHON

echo ""
echo "✅ Setup completado!"
echo ""
echo "Para ejecutar:"
echo "  source ~/granja-venv/bin/activate"
echo "  python3 app_simple.py"
echo ""
echo "Luego accede a: http://192.168.1.135:5000"
