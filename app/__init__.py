from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# 1. Inisialisasi extensions (tanpa menautkannya ke app secara langsung)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Pengaturan rute jika user belum login tapi mencoba akses halaman terproteksi
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'error'

def create_app(config_class=Config):
    # 2. Membuat instance aplikasi Flask
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 3. Menautkan extensions dengan aplikasi yang baru dibuat
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # 4. Mendaftarkan Blueprints (modular routing)
    # Import dilakukan di dalam fungsi untuk menghindari Circular Import
    from app.auth.routes import auth
    from app.main.routes import main
    from app.api.routes import api
    
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')  # Prefix untuk API

    return app