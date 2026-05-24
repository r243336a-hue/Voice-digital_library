# Voice-Navigable Digital Library - Setup & Deployment Guide

Complete guide to set up and run the Voice-Navigable Digital Library for visually impaired users.

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Local Development Setup](#local-development-setup)
3. [Project Structure](#project-structure)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)
8. [Development Workflow](#development-workflow)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.10 or higher
- **RAM**: 8 GB minimum (16 GB recommended for TTS model)
- **Disk Space**: 5 GB (for Python packages + TTS models)
- **Audio Device**: Microphone and speakers for voice interaction

### Optional
- **CUDA**: For GPU-accelerated TTS (NVIDIA GPUs only)
- **Docker**: For containerized deployment

---

## Local Development Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/r243336a-hue/Voice-digital_library.git
cd Voice-digital_library
```

### Step 2: Create a Python Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Upgrade pip

```bash
pip install --upgrade pip setuptools wheel
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

For development (with testing tools):
```bash
pip install -r requirements-dev.txt
```

### Step 5: Create Data Directories

```bash
mkdir -p data/raw data/cleaned data/database
mkdir -p logs audio_cache
```

### Step 6: Prepare Book Metadata

Edit `books_metadata.csv` with your books:

```csv
id,title,author,file_path,duration_seconds,language
1,Pride and Prejudice,Jane Austen,data/cleaned/pride_and_prejudice.txt,14400,en
2,The Great Gatsby,F. Scott Fitzgerald,data/cleaned/gatsby.txt,10800,en
```

**Columns:**
- `id`: Unique identifier
- `title`: Book title
- `author`: Author name
- `file_path`: Path to cleaned text file (relative to project root)
- `duration_seconds`: Approximate audiobook duration
- `language`: Language code (en, es, fr, etc.)

### Step 7: Initialize Database

```bash
python -c "from backend.db_utils import populate_from_csv; populate_from_csv('books_metadata.csv')"
```

---

## Project Structure

```
Voice-digital_library/
│
├── backend/                    # Python backend
│   ├── __init__.py
│   ├── app.py                 # Main Flask application
│   ├── search.py              # Search & retrieval logic
│   ├── intent.py              # Intent classification
│   ├── db_utils.py            # Database operations
│   ├── stt_utils.py           # Speech-to-text
│   ├── tts_utils.py           # Text-to-speech
│   ├── playback_engine.py     # Audio playback
│   └── config.py              # Configuration
│
├── frontend/                   # React/TypeScript UI
│   ├── components/
│   │   ├── book-card.tsx
│   │   ├── sidebar.tsx
│   │   ├── playback-controls.tsx
│   │   ├── search-bar.tsx
│   │   ├── voice-button.tsx
│   │   └── ...
│   ├── hooks/
│   │   ├── use-tts.ts
│   │   ├── use-speech-recognition.ts
│   │   └── use-toast.ts
│   └── index.html
│
├── data/                       # Data directory
│   ├── raw/                   # Raw book files (gitignored)
│   ├── cleaned/               # Cleaned text files (gitignored)
│   └── database/              # SQLite database (gitignored)
│
├── logs/                       # Application logs (gitignored)
│   ├── commands_*.csv
│   └── *.log
│
├── audio_cache/               # Cached audio files (gitignored)
│
├── docs/                       # Documentation
│   ├── ARCHITECTURE.md        # System design
│   ├── API.md                 # API documentation
│   └── USER_GUIDE.md          # User manual
│
├── tests/                      # Test suite
│   ├── test_search.py
│   ├── test_tts.py
│   └── test_intent.py
│
├── .github/                    # GitHub specific
│   └── workflows/             # CI/CD pipelines
│       └── tests.yml
│
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker compose
├── setup.py                   # Package setup
├── README.md                  # Project overview
├── SETUP.md                   # This file
└── LICENSE                    # Apache 2.0 License
```

---

## Configuration

### Backend Configuration (backend/config.py)

```python
import os
from pathlib import Path

class Config:
    """Base configuration"""
    BASE_DIR = Path(__file__).parent.parent
    
    # Database
    DATABASE_PATH = BASE_DIR / 'data' / 'database' / 'library.db'
    
    # TTS
    TTS_MODEL = 'tts_models/en/ljspeech/glow-tts'  # Fast model
    TTS_CACHE_DIR = BASE_DIR / 'audio_cache'
    
    # Speech Recognition
    SPEECH_LANG = 'en-US'
    
    # Logging
    LOG_DIR = BASE_DIR / 'logs'
    LOG_LEVEL = 'INFO'
    
    # Flask
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    DEBUG = False
    TTS_MODEL = 'tts_models/en/ljspeech/tacotron2-DDC'  # Higher quality

class TestingConfig(Config):
    TESTING = True
    DATABASE_PATH = ':memory:'
```

### Environment Variables

Create a `.env` file (not committed to Git):

```bash
# Flask
FLASK_ENV=development
FLASK_DEBUG=1

# Database
DATABASE_URL=sqlite:///data/database/library.db

# TTS
TTS_USE_GPU=0  # Set to 1 if you have CUDA

# Speech Recognition
SPEECH_RECOGNITION_API_KEY=your_key_here

# Server
HOST=127.0.0.1
PORT=5000
```

---

## Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
# Activate venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Set environment
export FLASK_ENV=development  # or set FLASK_ENV=development on Windows
export FLASK_DEBUG=1

# Run Flask app
cd backend
python app.py
# Backend runs on http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
# Frontend runs on http://localhost:3000
# (Configure based on your frontend setup - React, Vue, etc.)
```

### Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_search.py -v

# Run with coverage
pytest --cov=backend tests/
```

### Production Mode

Using Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

---

## Deployment

### Docker Deployment

**Build the image:**
```bash
docker build -t voice-library:latest .
```

**Run the container:**
```bash
docker run -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  voice-library:latest
```

### Docker Compose

```bash
docker-compose up -d
```

### Cloud Deployment (Heroku Example)

1. Create `Procfile`:
```
web: gunicorn -w 4 backend.app:app
```

2. Deploy:
```bash
heroku create your-app-name
heroku config:set FLASK_ENV=production
git push heroku main
```

### Raspberry Pi / Low-Power Devices

Use a lightweight TTS model:
```python
TTS_MODEL = 'tts_models/en/ljspeech/glow-tts'  # Smallest model
```

---

## Troubleshooting

### Issue: TTS Model Download Takes Too Long

**Solution:**
- Download the model manually:
  ```bash
  python -c "from TTS.api import TTS; tts = TTS(model_name='tts_models/en/ljspeech/glow-tts', gpu=False); print('Model downloaded')"
  ```

### Issue: Microphone Not Detected

**Solution (Windows):**
```bash
pip install pyaudio
# Or use WinSound (built-in)
```

**Solution (Linux):**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**Solution (macOS):**
```bash
brew install portaudio
pip install pyaudio
```

### Issue: Database Lock Error

**Solution:**
```bash
# Close all connections and delete the lock file
rm data/database/library.db-journal
```

### Issue: Out of Memory with TTS

**Solution:**
- Use GPU acceleration (if available):
  ```python
  TTS_USE_GPU = True
  ```
- Use a smaller model:
  ```python
  TTS_MODEL = 'tts_models/en/ljspeech/glow-tts'
  ```

### Issue: Port Already in Use

**Solution:**
```bash
# Find and kill the process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows
```

---

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/my-feature
```

### 2. Make Changes

```bash
# Edit files
git add .
git commit -m "Add my feature"
```

### 3. Run Tests

```bash
pytest tests/ -v
```

### 4. Push and Create PR

```bash
git push origin feature/my-feature
```

### 5. Code Review & Merge

After review:
```bash
git checkout main
git merge feature/my-feature
git push origin main
```

---

## Additional Resources

- **TTS Models**: [Coqui TTS Documentation](https://github.com/coqui-ai/TTS)
- **Speech Recognition**: [SpeechRecognition Docs](https://github.com/Uberi/speech_recognition)
- **Flask**: [Flask Documentation](https://flask.palletsprojects.com/)
- **Accessibility**: [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

## Support

For issues and questions:
1. Check existing [Issues](https://github.com/r243336a-hue/Voice-digital_library/issues)
2. Create a new issue with:
   - OS and Python version
   - Steps to reproduce
   - Error messages and logs

---

**Last Updated**: May 2026
**License**: Apache 2.0
