"""
Arquivo de configuração da aplicação
Você pode modificar as constantes aqui conforme necessário
"""

import os

# Diretório base da aplicação
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Configurações do Flask
DEBUG = True
TESTING = False

# Configurações do Banco de Dados
SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASEDIR, "instance", "sofascore.db")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Upload de Arquivos
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB
UPLOAD_FOLDER = os.path.join(BASEDIR, 'app', 'static', 'uploads')
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm', 'avi', 'mkv'}

# Configurações de Segurança
SECRET_KEY = 'sua-chave-secreta-aqui'  # Mude em produção!

# Paginação
ITEMS_PER_PAGE = 20

# Timeout de Sessão
PERMANENT_SESSION_LIFETIME = 3600  # 1 hora

# Locale
BABEL_DEFAULT_LOCALE = 'pt_BR'

# Logging
LOG_LEVEL = 'INFO'
