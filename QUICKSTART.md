# Quick Start Guide - 5 Minutes to Running System

## TL;DR - Fastest Setup

```bash
# 1. Create and enter directory
mkdir showcase-remodels-rag && cd showcase-remodels-rag

# 2. Create virtual environment
python3 -m venv venv && source venv/bin/activate

# 3. Install dependencies (copy requirements.txt first)
pip install flask flask-cors torch transformers sentence-transformers chromadb pillow opencv-python scikit-learn

# 4. Copy all code files to correct locations (see structure below)

# 5. Run setup
python setup.py

# 6. Start API
python api/app.py

# 7. In another terminal, open frontend
python -m http.server 8000 --directory frontend
# Visit: http://localhost:8000
```

## File Placement Guide

After creating the project folder, place files exactly as shown:

```
showcase-remodels-rag/
│
├── input.txt                    ← Your existing knowledge base
├── requirements.txt             ← Dependencies file
├── setup.py                     ← Setup script
│
├── rag/
│   ├── __init__.py             ← Empty file (create it)
│   ├── vector_store.py         ← Vector database code
│   ├── image_analyzer.py       ← Image analysis code
│   ├── rag_generator.py        ← RAG response generator
│   └── tokenizer_advanced.py   ← Advanced tokenizer
│
├── api/
│   ├── __init__.py             ← Empty file (create it)
│   └── app.py                  ← Flask API server
│
├── frontend/
│   └── index.html              ← Web interface
│
└── scripts/
    ├── init_database.py        ← Database initialization
    └── test_system.py          ← System testing
```

## Essential Commands

### Start Everything

**Terminal 1 - API Server:**
```bash
cd showcase-remodels-rag
source venv/bin/activate  # or venv\Scripts\activate on Windows
python api/app.py
```

**Terminal 2 - Frontend:**
```bash
cd showcase-remodels-rag/frontend
python -m http.server 8000
```

**Browser:**
```
http://localhost:8000
```

### Test It Works

**Test API:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What services do you offer?"}'
```

**Test Web Interface:**
1. Go to http://localhost:8000
2. Type: "Tell me about bathroom remodeling"
3. Click Send
4. Should get a detailed response!

## What's Different from Your Original System?

### ✅ Major Improvements

1. **RAG System**: Now uses vector database for accurate responses
2. **Better Tokenization**: Subword tokenization instead of character-level
3. **Image Analysis**: Actual room detection and feature extraction
4. **Web Interface**: Modern, responsive chat UI
5. **API Architecture**: RESTful API for easy integration
6. **No Training Required**: Works immediately with your knowledge base

### 🔄 What You Keep

- Your existing `input.txt` knowledge base
- The home remodeling business logic
- Your training data and domain knowledge

### ❌ What You Can Remove

- `chat.py` (replaced by `api/app.py`)
- `tokenizer.py` (replaced by `tokenizer_advanced.py`)
- `train.py` (no longer needed - RAG doesn't require training)
- `remodel_assistant.py` (functionality now in `rag_generator.py`)

## Key Features Demo

### 1. Text Chat
```
You: "What are your bathroom services?"
Bot: [Retrieves relevant info from vector DB and generates response]
```

### 2. Image Upload
```
Upload: bathroom-photo.jpg
You: "What improvements do you suggest?"
Bot: [Analyzes image, detects fixtures, suggests improvements]
```

### 3. Conversation History
```
Each conversation is tracked with a unique ID
Can retrieve full conversation history via API
```

## Architecture Overview

```
┌─────────────┐
│   Browser   │
│  (Frontend) │
└──────┬──────┘
       │ HTTP
       ↓
┌──────────────┐
│  Flask API   │ ← REST endpoints
│   (Backend)  │
└──────┬───────┘
       │
       ├─→ Vector Store (ChromaDB) ← Knowledge retrieval
       │
       ├─→ Image Analyzer ← Room detection
       │
       └─→ RAG Generator ← Response generation
```

## Troubleshooting Quick Fixes

**Problem: "Module not found"**
```bash
pip install -r requirements.txt
```

**Problem: "Port already in use"**
```bash
# Change port in .env or:
python api/app.py --port 5001
```

**Problem: "Database not initialized"**
```bash
python scripts/init_database.py
```

**Problem: "CORS error"**
```bash
pip install flask-cors
```

## Configuration Tweaks

Edit `.env` file (created by setup.py):

```bash
# Make responses more creative
TEMPERATURE=0.9

# Make responses longer
MAX_TOKENS=500

# Enable YOLO for better image analysis
USE_YOLO=True

# Change API port
API_PORT=5001
```

## Performance Tips

**Faster Startup:**
- Keep `USE_YOLO=False`
- Use smaller embedding model

**Better Responses:**
- Increase `MAX_TOKENS`
- Adjust `TEMPERATURE`
- Add more content to `input.txt`

**Production Ready:**
- Set `FLASK_DEBUG=False`
- Use gunicorn: `gunicorn api.app:app`
- Enable authentication

## Common Use Cases

### Update Knowledge Base
1. Edit `input.txt`
2. Run: `python scripts/init_database.py`
3. Restart API server

### Add New Endpoints
1. Edit `api/app.py`
2. Add route function
3. Restart server

### Customize Frontend
1. Edit `frontend/index.html`
2. Refresh browser (no restart needed)

### Export Conversation
```bash
curl http://localhost:5000/api/conversation/<id>
```

## Next Steps

1. ✅ **Test basic functionality** - Chat and image upload
2. ✅ **Customize responses** - Edit temperature and tokens
3. ✅ **Add more knowledge** - Expand input.txt
4. ✅ **Deploy** - See deployment guide for production
5. ✅ **Monitor** - Check logs for errors and usage

## Resources

- **Full Installation**: See `INSTALLATION.md`
- **Project Structure**: See `PROJECT_STRUCTURE.md`
- **API Documentation**: Check `api/app.py` comments
- **Code Examples**: See `scripts/test_system.py`

## Support

If something doesn't work:
1. Check you're in virtual environment: `which python`
2. Verify all files are in correct locations
3. Check API logs for error messages
4. Ensure ports 5000 and 8000 are available

---

**You're ready to go! 🚀**

Start the API server and frontend, then visit http://localhost:8000 to try your new AI assistant!