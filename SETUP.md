# Voice-Navigable Digital Library - Setup & Deployment Guide

Complete guide to set up and run the Voice-Navigable Digital Library for visually impaired users.

## 📋 Table of Contents

1. System Requirements
2. Local Development Setup
3. Project Structure
4. Configuration
5. Running the Application
6. Deployment
7. Troubleshooting
8. Development Workflow

---

## System Requirements
- OS: Windows 10+, macOS 10.14+, or Ubuntu 18.04+
- Python: 3.10 or higher
- RAM: 8 GB min (16 GB rec.)
- Audio: Microphone & speakers
- Docker (optional, for containerized deployment or production)

---

## Local Development Setup

1. **Clone the repository**
   ```sh
   git clone https://github.com/r243336a-hue/Voice-digital_library.git
   cd Voice-digital_library
   ```
2. **Create virtual environment**
   - Windows:
     ```sh
     python -m venv venv
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```
3. **Install requirements**
   ```sh
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```
4. **Create directory structure**
   ```sh
   mkdir -p data/raw data/cleaned data/database logs audio_cache
   ```
5. **Add/Edit books_metadata.csv** (see books_metadata.csv.example)
6. **Populate the SQLite DB**
   ```sh
   python -c "from backend.db_utils import populate_from_csv; populate_from_csv('books_metadata.csv')"
   ```
7. **Run the backend**
   ```sh
   python backend/app.py
   ```
8. **Run the frontend**
   - (Configure based on your actual frontend setup; e.g. npm start for React)

---

## Project Structure

```text
Voice-digital_library/
│
├── backend/
│   ├── app.py
│   ├── search.py
│   ├── intent.py
│   ├── db_utils.py
│   ├── stt_utils.py
│   ├── tts_utils.py
│   └── playback_engine.py
├── frontend/
│   ├── components/
│   └── hooks/
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── database/
├── logs/
├── audio_cache/
├── tests/
├── docs/
├── .github/
│   └── workflows/
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
├── SETUP.md
└── LICENSE
```

---

## Configuration

### .env File
Create a `.env` file (not committed):
```env
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=sqlite:///data/database/library.db
TTS_USE_GPU=0
```

---

## Running the Application

### Backend (Flask)
```sh
source venv/bin/activate  # or venv\Scripts\activate
python backend/app.py
```

### Frontend (React)
See the /frontend directory for running the React app (typically `npm install && npm start`).

---

## Deployment

### Docker
```sh
docker build -t voice-library:latest .
docker run -p 5000:5000 \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/logs:/app/logs \
    voice-library:latest
```

### Docker Compose
```sh
docker-compose up -d
```

---

## Troubleshooting

### TTS Model Slow?
- First run downloads the model. Cache is in `audio_cache/`.
- Use a smaller TTS model if needed (see ARCHITECTURE.md).

### Microphone Not Detected?
- Install system dependencies: `pip install pyaudio` (plus system `portaudio` on Linux/macOS).

### Database Locked?
- Delete any `library.db-journal` files in `data/database/` and restart.

---

## Development Workflow

1. Branch from `main`: `git checkout -b feature/short-desc`
2. Make changes, run tests, commit and push.
3. Open a pull request, fill out PR template, ensure CI passes.
4. Wait for review and merge.

---

For more detail, see [ARCHITECTURE.md](ARCHITECTURE.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
