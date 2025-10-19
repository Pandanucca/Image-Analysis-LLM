# Installation Guide - Showcase Remodels RAG System

## Prerequisites

- Python 3.8 or higher
- pip package manager
- 4GB+ RAM recommended
- 2GB+ free disk space

## Step-by-Step Installation

### 1. Create Project Directory

```bash
mkdir showcase-remodels-rag
cd showcase-remodels-rag
```

### 2. Set Up Virtual Environment

**On Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Create Project Structure

Create the following files and folders in your project directory:

```
showcase-remodels-rag/
├── requirements.txt
├── setup.py
├── input.txt (your existing knowledge base)
├── rag/
│   ├── __init__.py
│   ├── vector_store.py
│   ├── image_analyzer.py
│   ├── rag_generator.py
│   └── tokenizer_advanced.py
├── api/
│   ├── __init__.py
│   ├── app.py
│   └── config.py
├── frontend/
│   └── index.html
├── scripts/
│   ├── init_database.py
│   └── test_system.py
└── models/
```

### 4. Copy Code Files

Copy all the provided code files into their respective directories:

1. **requirements.txt** → root directory
2. **setup.py** → root directory
3. **rag/vector_store.py** → rag/ folder
4. **rag/image_analyzer.py** → rag/ folder
5. **rag/rag_generator.py** → rag/ folder
6. **rag/tokenizer_advanced.py** → rag/ folder
7. **api/app.py** → api/ folder
8. **frontend/index.html** → frontend/ folder
9. **input.txt** (your existing file) → root directory

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** This may take 5-10 minutes depending on your internet connection.

If you encounter installation issues:

**For PyTorch (if needed):**
```bash
# CPU only version (lighter)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# GPU version (if you have CUDA)
pip install torch torchvision torchaudio
```

**For scikit-learn (needed by image_analyzer.py):**
```bash
pip install scikit-learn
```

### 6. Run Setup Script

```bash
python setup.py
```

This will:
- Create necessary directories
- Generate .env configuration file
- Create .gitignore
- Initialize the vector database
- Verify all components

### 7. Verify Installation

Test the system:

```bash
python scripts/test_system.py
```

You should see output showing successful queries and responses.

### 8. Start the API Server

```bash
python api/app.py
```

You should see:
```
Showcase Remodels API Server
========================================
Endpoints:
  POST /api/chat - Text chat
  POST /api/chat/image - Chat with image upload
  ...
 * Running on http://0.0.0.0:5000
```

### 9. Open the Web Interface

**Option A: Direct file access**
```bash
# Simply open frontend/index.html in your web browser
```

**Option B: Local web server (recommended)**
```bash
# In a new terminal window:
cd frontend
python -m http.server 8000
```

Then visit: **http://localhost:8000**

## Testing the Installation

### Test 1: API Health Check

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "..."}
```

### Test 2: Text Chat

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What services do you offer?"}'
```

### Test 3: Web Interface

1. Open http://localhost:8000 in your browser
2. Type a question: "What are your bathroom remodeling options?"
3. Click Send
4. You should receive a detailed response

### Test 4: Image Upload

1. In the web interface, click the upload button
2. Select a room image
3. Type: "What improvements would you suggest?"
4. Click Send
5. You should receive analysis and suggestions

## Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: Port 5000 already in use

**Solution:**
Edit `.env` file and change:
```
API_PORT=5001
```

Or kill the process using port 5000:
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: Vector database initialization fails

**Solution:**
```bash
# Manually initialize database
python scripts/init_database.py

# Or delete and reinitialize
rm -rf chroma_db
python setup.py
```

### Issue: Image analysis not working

**Solution:**
Install missing dependencies:
```bash
pip install scikit-learn opencv-python pillow
```

### Issue: CORS errors in browser

**Solution:**
Make sure flask-cors is installed:
```bash
pip install flask-cors
```

### Issue: Out of memory errors

**Solution:**
Reduce batch sizes in `.env`:
```
MAX_TOKENS=150
```

## Optional: Install YOLO for Advanced Image Analysis

```bash
pip install ultralytics

# In .env file, set:
USE_YOLO=True
```

The first time you run image analysis, YOLO will download (~6MB).

## Configuration Options

Edit `.env` file to customize:

```bash
# API Settings
API_PORT=5000                    # Change API port
FLASK_DEBUG=True                 # Enable/disable debug mode

# Model Settings
EMBEDDING_MODEL=all-MiniLM-L6-v2  # Change embedding model
USE_YOLO=False                    # Enable YOLO object detection
TEMPERATURE=0.7                   # Response creativity (0.0-1.0)
MAX_TOKENS=300                    # Maximum response length

# Database
CHROMA_DB_PATH=./chroma_db       # Vector database location
```

## Performance Optimization

### For Faster Startup:
1. Use CPU-only PyTorch (lighter)
2. Keep USE_YOLO=False
3. Use smaller embedding model

### For Better Responses:
1. Increase MAX_TOKENS to 400-500
2. Adjust TEMPERATURE (higher = more creative)
3. Use larger embedding model like 'all-mpnet-base-v2'

### For Production:
1. Set FLASK_DEBUG=False
2. Use a production WSGI server (gunicorn)
3. Enable HTTPS
4. Add authentication

## Next Steps

1. **Customize Knowledge Base**: Edit `input.txt` with your specific content
2. **Test Thoroughly**: Try various queries and image uploads
3. **Adjust Responses**: Tune temperature and max_tokens in `.env`
4. **Deploy**: See deployment guide for production setup

## Getting Help

If you encounter issues:
1. Check the logs in `logs/` directory
2. Run with debug mode: `FLASK_DEBUG=True python api/app.py`
3. Review error messages carefully
4. Check that all files are in correct locations

## Quick Commands Reference

```bash
# Activate environment
source venv/bin/activate

# Start API server
python api/app.py

# Start frontend server
python -m http.server 8000 --directory frontend

# Test system
python scripts/test_system.py

# Reinitialize database
python scripts/init_database.py

# Install/update dependencies
pip install -r requirements.txt --upgrade
```

## System Requirements

**Minimum:**
- Python 3.8+
- 4GB RAM
- 2GB disk space
- CPU only

**Recommended:**
- Python 3.9+
- 8GB RAM
- 5GB disk space
- GPU (for faster processing)

**Tested On:**
- Ubuntu 20.04+
- macOS 11+
- Windows 10/11

Installation complete! You're ready to use the Showcase Remodels AI Assistant.