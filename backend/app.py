import os
import webbrowser
from flask import Flask, send_from_directory
from flask_cors import CORS
from models import db
from routes import creditos_bp

app = Flask(__name__)
CORS(app)

# Guarda la base de datos directamente en /backend en lugar de /instance
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'creditos.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(creditos_bp)

# 📌 Ruta para servir el frontend (index.html)
@app.route('/')
def servir_frontend():
    frontend_path = os.path.abspath(os.path.join(BASE_DIR, '../frontend'))
    return send_from_directory(frontend_path, 'index.html')

# 📌 Ruta para servir archivos estáticos (CSS, JS, imágenes)
@app.route('/<path:path>')
def static_files(path):
    frontend_path = os.path.abspath(os.path.join(BASE_DIR, '../frontend'))
    return send_from_directory(frontend_path, path)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # 📌 Abre automáticamente el navegador en la URL correcta
    webbrowser.open('http://127.0.0.1:5000/')
    
    app.run(debug=True)
