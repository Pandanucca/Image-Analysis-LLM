"""
Setup script for Showcase Remodels RAG System.
Run this after installing requirements.txt to initialize the system.
"""

import os
import sys
from pathlib import Path
import subprocess


class SetupManager:
    def __init__(self):
        self.project_root = Path.cwd()
        self.steps_completed = []

    def print_header(self, text):
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)

    def print_step(self, step, status=""):
        print(f"[{len(self.steps_completed) + 1}] {step}... {status}")

    def create_directories(self):
        """Create necessary project directories."""
        self.print_step("Creating project directories")

        directories = [
            'rag',
            'api',
            'frontend',
            'models',
            'uploads',
            'chroma_db',
            'scripts',
            'tests',
            'logs'
        ]

        for dir_name in directories:
            dir_path = self.project_root / dir_name
            dir_path.mkdir(exist_ok=True)

            # Create __init__.py for Python packages
            if dir_name in ['rag', 'api', 'tests']:
                init_file = dir_path / '__init__.py'
                if not init_file.exists():
                    init_file.touch()

            # Create .gitkeep for empty directories
            if dir_name in ['uploads', 'chroma_db', 'models', 'logs']:
                gitkeep = dir_path / '.gitkeep'
                if not gitkeep.exists():
                    gitkeep.touch()

        self.steps_completed.append("directories")
        print("✓ Directories created")

    def create_env_file(self):
        """Create .env file if it doesn't exist."""
        self.print_step("Creating environment configuration")

        env_file = self.project_root / '.env'
        if env_file.exists():
            print("✓ .env file already exists")
            self.steps_completed.append("env")
            return

        env_content = """# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=5000
SECRET_KEY=your-secret-key-here-change-in-production

# Model Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
USE_YOLO=False
TEMPERATURE=0.7
MAX_TOKENS=300

# Database
CHROMA_DB_PATH=./chroma_db

# Logging
LOG_LEVEL=INFO
"""

        with open(env_file, 'w') as f:
            f.write(env_content)

        self.steps_completed.append("env")
        print("✓ .env file created")

    def create_gitignore(self):
        """Create .gitignore file."""
        self.print_step("Creating .gitignore")

        gitignore_file = self.project_root / '.gitignore'

        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# Environment Variables
.env
.env.local

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Project Specific
uploads/*
!uploads/.gitkeep
chroma_db/*
!chroma_db/.gitkeep
models/*.pt
logs/*.log

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/
"""

        with open(gitignore_file, 'w') as f:
            f.write(gitignore_content)

        self.steps_completed.append("gitignore")
        print("✓ .gitignore created")

    def check_dependencies(self):
        """Check if all dependencies are installed."""
        self.print_step("Checking dependencies")

        required_packages = [
            'flask',
            'torch',
            'transformers',
            'sentence_transformers',
            'chromadb',
            'pillow',
            'opencv-python'
        ]

        missing = []
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing.append(package)

        if missing:
            print(f"⚠ Missing packages: {', '.join(missing)}")
            print("  Run: pip install -r requirements.txt")
            return False

        self.steps_completed.append("dependencies")
        print("✓ All dependencies installed")
        return True

    def check_knowledge_base(self):
        """Check if knowledge base file exists."""
        self.print_step("Checking knowledge base")

        kb_file = self.project_root / 'input.txt'
        if not kb_file.exists():
            print("⚠ input.txt not found")
            print("  Please add your knowledge base file as 'input.txt'")
            return False

        # Check file size
        size_kb = kb_file.stat().st_size / 1024
        print(f"✓ Knowledge base found ({size_kb:.1f} KB)")

        self.steps_completed.append("knowledge_base")
        return True

    def initialize_database(self):
        """Initialize vector database with knowledge base."""
        self.print_step("Initializing vector database")

        try:
            from rag.vector_store import VectorStore, ingest_knowledge_base

            vs = VectorStore(collection_name="remodeling_kb")

            # Check if already populated
            if vs.collection.count() > 0:
                print(f"✓ Database already initialized ({vs.collection.count()} documents)")
                self.steps_completed.append("database")
                return True

            # Ingest knowledge base
            print("  Ingesting knowledge base...")
            ingest_knowledge_base(vs, "input.txt")

            print(f"✓ Database initialized ({vs.collection.count()} documents)")
            self.steps_completed.append("database")
            return True

        except Exception as e:
            print(f"✗ Error initializing database: {e}")
            return False

    def create_readme(self):
        """Create README.md file."""
        self.print_step("Creating README")

        readme_file = self.project_root / 'README.md'

        readme_content = """# Showcase Remodels AI Assistant

RAG-based chatbot for home remodeling consultations with image analysis capabilities.

## Features

- 🏠 Natural language Q&A about remodeling services
- 📸 Image upload and room analysis
- 🔍 Retrieval-Augmented Generation for accurate responses
- 💬 Web-based chat interface
- 📊 Vector database for efficient knowledge retrieval

## Quick Start

1. **Start the API server:**
```bash
python api/app.py
```

2. **Open the web interface:**
```bash
# Open frontend/index.html in your browser, or serve with:
python -m http.server 8000 --directory frontend
```

3. **Visit:** http://localhost:8000

## API Endpoints

- `POST /api/chat` - Text chat
- `POST /api/chat/image` - Chat with image upload
- `GET /api/conversation/<id>` - Get conversation history
- `POST /api/search` - Search knowledge base

## Project Structure

```
showcase-remodels-rag/
├── rag/              # RAG system core
├── api/              # Flask API backend
├── frontend/         # Web interface
├── models/           # Model storage
├── uploads/          # User uploads
└── chroma_db/        # Vector database
```

## Testing

```bash
# Test complete system
python scripts/test_system.py

# Test API
curl -X POST http://localhost:5000/api/chat \\
  -H "Content-Type: application/json" \\
  -d '{"query": "What services do you offer?"}'
```

## Configuration

Edit `.env` file to configure:
- API port
- Model settings
- Database paths

## Contact

Showcase Remodels
- Phone: 888-691-4969
- Website: https://showcaseremodels.com
- Location: Turnersville, NJ
"""

        with open(readme_file, 'w') as f:
            f.write(readme_content)

        self.steps_completed.append("readme")
        print("✓ README.md created")

    def run_setup(self):
        """Run complete setup process."""
        self.print_header("Showcase Remodels RAG System Setup")

        print("\nThis script will set up your project structure and initialize")
        print("the RAG system for the home remodeling chatbot.\n")

        # Run setup steps
        self.create_directories()
        self.create_env_file()
        self.create_gitignore()
        self.create_readme()

        deps_ok = self.check_dependencies()
        kb_ok = self.check_knowledge_base()

        if deps_ok and kb_ok:
            self.initialize_database()

        # Print summary
        self.print_header("Setup Complete!")

        print(f"\n✓ Completed {len(self.steps_completed)} steps")
        print("\nNext steps:")
        print("1. Review and update .env configuration")
        print("2. Start the API server: python api/app.py")
        print("3. Open frontend/index.html in your browser")
        print("\nFor detailed information, see README.md")

        if not deps_ok:
            print("\n⚠ Don't forget to install dependencies:")
            print("  pip install -r requirements.txt")

        if not kb_ok:
            print("\n⚠ Don't forget to add your input.txt file")


if __name__ == "__main__":
    setup = SetupManager()
    setup.run_setup()