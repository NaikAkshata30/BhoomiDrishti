import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


def build_db_uri(user, password, host, port, name):
    """Build a safe SQLAlchemy URL while escaping special characters in credentials."""
    user = quote_plus(user or '')
    password = quote_plus(password or '')
    host = host or 'localhost'
    name = quote_plus(name or '')
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"


class Config:
    """Base configuration"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')


def normalize_database_url(value):
    """Normalize provider URLs into SQLAlchemy-compatible connection strings."""
    if not value:
        return None
    if value.startswith('mysql://'):
        return value.replace('mysql://', 'mysql+pymysql://', 1)
    if value.startswith('postgres://'):
        return value.replace('postgres://', 'postgresql://', 1)
    return value


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    
    # Database
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'land_acquisition_db')
    
    # SQLAlchemy URI
    if DB_PASSWORD:
        SQLALCHEMY_DATABASE_URI = build_db_uri(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
    else:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{quote_plus(DB_USER)}@{DB_HOST}:{DB_PORT}/{quote_plus(DB_NAME)}"


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # Database
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    
    # SQLAlchemy URI
    SQLALCHEMY_DATABASE_URI = normalize_database_url(
        os.getenv('DATABASE_URL') or os.getenv('MYSQL_URL')
    ) or build_db_uri(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development').lower()
    
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig
