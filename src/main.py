from flask import Flask
from dotenv import load_dotenv
import os
from app.db.base import engine, Base
from app.models import documento_db 

load_dotenv()

Base.metadata.create_all(bind=engine)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '10X_SECRET_KEY')

    # Registro de Blueprints
    from app.api.routes.documentos import bp as documentos_bp
    app.register_blueprint(documentos_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    print("Rutas registradas:")
    print(app.url_map)
    app.run(host='0.0.0.0', port=5000, debug=True)