import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
     # Google Cloud PostgreSQL Database Configuration
    DB_USER = os.environ.get('DB_USER', 'booknerd')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST', '34.130.181.235')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'bookinfo')
    
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenLibrary API Configuration
    OPENLIBRARY_BASE_URL = 'https://openlibrary.org'
    OPENLIBRARY_COVERS_URL = 'https://covers.openlibrary.org'