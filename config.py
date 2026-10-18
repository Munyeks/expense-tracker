import os
from dotenv import load_dotenv

# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Proteksi keamanan dasar & CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback_secret_key_jika_env_gagal'
    
    # Konfigurasi PostgreSQL via SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Mematikan fitur event system SQLAlchemy yang memakan memori
    SQLALCHEMY_TRACK_MODIFICATIONS = False