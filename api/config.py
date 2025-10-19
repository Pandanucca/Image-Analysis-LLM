import os
from pathlib import Path


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    UPLOAD_FOLDER = Path('uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # RAG Configuration
    VECTOR_DB_PATH = os.environ.get('CHROMA_DB_PATH', './chroma_db')
    EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')

    # Knowledge Base
    KNOWLEDGE_BASE_PATH = 'input.txt'