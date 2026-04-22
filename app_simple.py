#!/usr/bin/env python3
"""
Hola Mundo - Test básico Flask
Para verificar que la Raspberry funciona
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hola():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🌾 Granja IoT</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
            }
            .container {
                text-align: center;
                color: white;
            }
            h1 { font-size: 3em; margin: 0; }
            p { font-size: 1.5em; margin: 20px 0; }
            .info {
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌾 ¡Hola Mundo!</h1>
            <div class="info">
                <p>✅ Flask funciona correctamente</p>
                <p>🚀 Raspberry Pi Online</p>
                <p style="font-size: 0.9em; opacity: 0.8;">Sistema listo para producción</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/api/status')
def status():
    return {'status': 'ok', 'sistema': 'granja-iot'}

if __name__ == '__main__':
    print("🌾 Granja IoT - Hola Mundo")
    print("📡 Escuchando en http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
