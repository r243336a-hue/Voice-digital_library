# System Architecture

## Overview

Voice-Navigable Digital Library is a web-based application that provides voice-controlled access to digital books for visually impaired users. The system uses speech-to-text (STT) for voice commands, natural language processing for intent classification, and text-to-speech (TTS) for audio feedback.

```
┌─────────────────────────────────────────────────────────────┐
│                    User (Visually Impaired)                 │
│                   (Microphone + Speakers)                   │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   ┌────▼────┐            ┌──────▼──────┐
   │  Voice  │            │  Frontend   │
   │ Input   │            │   (React)   │
   │  (STT)  │            │             │
   └────┬────┘            └──────┬──────┘
        │                         │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │   Backend (Flask API)   │
        │                         │
        │ ┌─────────────────────┐ │
        │ │  Intent Classifier  │ │
        │ │  (Rule-based/ML)    │ │
        │ └─────────────────────┘ │
        │                         │
        │ ┌─────────────────────┐ │
        │ │  Search Engine      │ │
        │ │  (Fuzzy Matching)   │ │
        │ └─────────────────────┘ │
        │                         │
        │ ┌─────────────────────┐ │
        │ │  Playback Engine    │ │
        │ │  (TTS + Audio)      │ │
        │ └─────────────────────┘ │
        │                         │
        │ ┌─────────────────────┐ │
        │ │  Database Layer     │ │
        │ │  (SQLite)           │ │
        │ └─────────────────────┘ │
        │                         │
        └────────────┬────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   ┌────▼────┐            ┌──────▼──────┐
   │   TTS   │            │   Database  │
   │ Service │            │  (SQLite)   │
   │         │            │             │
   └─────────┘            └─────────────┘
```

## Component Details

### Frontend (React/TypeScript)

**Purpose**: User interface accessible via keyboard and screen reader

**Key Components**:
- `search-bar.tsx`: Voice/text search input
- `book-card.tsx`: Book preview and metadata
- `playback-controls.tsx`: Play, pause, resume, stop controls
- `sidebar.tsx`: Navigation and options
- `voice-button.tsx`: Voice command trigger

**Hooks**:
- `use-speech-recognition.ts`: Captures audio from microphone
- `use-tts.ts`: Sends text to backend for audio synthesis
- `use-toast.ts`: User notifications

**API Endpoint**: `http://localhost:5000/api`

### Backend (Flask)

**Purpose**: Core application logic, database management, and API

#### 1. **Intent Classification (`intent.py`)**

Identifies user intent from transcribed text:

```
Input: "Play pride and prejudice"
  ↓
Intent: PLAY
Entities: {title: "pride and prejudice"}
  ↓
Output: {"intent": "PLAY", "entities": {...}}
```

**Supported Intents**:
- `SEARCH`: Find books by title/author
- `PLAY`: Start audio playback
- `PAUSE`: Pause current playback
- `RESUME`: Resume paused playback
- `STOP`: Stop playback
- `NEXT_CHAPTER`: Move to next chapter
- `PREVIOUS_CHAPTER`: Move to previous chapter
- `HELP`: Request assistance

**Implementation**: Rule-based with optional ML classifier

#### 2. **Search Engine (`search.py`)**

Finds books using fuzzy matching and metadata:

```python
# Fuzzy matching algorithm
query = "pridee nd prejjudice"
results = fuzzy_search(query, book_titles)
# Returns: [{"id": 1, "title": "Pride and Prejudice", "match_score": 0.92}]
```

**Features**:
- Fuzzy matching (handles typos)
- Author search
- Genre filtering
- Full-text search (optional)

**Database Query**:
```sql
SELECT * FROM books 
WHERE title LIKE '%query%' OR author LIKE '%query%'
ORDER BY relevance_score DESC
LIMIT 10
```

#### 3. **Playback Engine (`playback_engine.py`)**

Manages audio playback and user controls:

```
Book Text → TTS Service → Audio Stream → Speaker
                ↑
          (Segment by ~5 min chunks)
```

**Features**:
- Stream long-form audio without full download
- Control: play, pause, resume, skip
- Progress tracking
- Bookmarking (save position)

#### 4. **TTS Service (`tts_utils.py`)**

Converts text to speech using Coqui TTS:

```python
from TTS.api import TTS

tts = TTS(model_name="tts_models/en/ljspeech/glow-tts")
wav = tts.tts(text="Hello world")
# Output: numpy array (audio waveform)
```

**Models Available**:
- `glow-tts`: Fast, low-resource (recommended)
- `tacotron2-DDC`: Higher quality
- `vits`: Fast with good quality

**Caching**: Audio is cached to avoid re-synthesis

#### 5. **Speech Recognition (`stt_utils.py`)**

Converts audio to text:

```python
from speech_recognition import Microphone, Recognizer

recognizer = Recognizer()
with Microphone() as source:
    audio = recognizer.listen(source)
    text = recognizer.recognize_google(audio)
```

**Options**:
- Google Speech Recognition (free, cloud-based)
- Vosk (offline, low-quality)
- AssemblyAI (paid, high-quality)

#### 6. **Database (`db_utils.py`)**

SQLite database for book metadata:

```
Books Table:
┌────┬─────────────────────┬─────────────────┬──────────────────┐
│ id │ title               │ author          │ file_path        │
├────┼─────────────────────┼─────────────────┼──────────────────┤
│ 1  │ Pride and Prejudice │ Jane Austen     │ data/cleaned/... │
│ 2  │ The Great Gatsby    │ F. Scott Fitz.. │ data/cleaned/... │
└────┴─────────────────────┴─────────────────┴──────────────────┘

ReadingProgress Table:
┌────┬────────┬──────────┬──────────────┐
│ id │ book_id│ position │ last_updated │
├────┼────────┼──────────┼──────────────┤
│ 1  │ 1      │ 12500    │ 2026-05-24   │
└────┴────────┴──────────┴──────────────┘
```

### Data Flow

#### Scenario 1: Search for a Book

```
1. User speaks: "Find pride and prejudice"
              ↓
2. STT converts to text → "find pride and prejudice"
              ↓
3. Intent classifier → Intent: SEARCH, Entity: {title: "pride and prejudice"}
              ↓
4. Search engine finds matching books
              ↓
5. TTS converts results to speech → "Found: Pride and Prejudice by Jane Austen"
              ↓
6. User hears results through speaker
```

#### Scenario 2: Play a Book

```
1. User speaks: "Play pride and prejudice"
              ↓
2. STT → "play pride and prejudice"
              ↓
3. Intent classifier → Intent: PLAY, Entity: {title: "pride and prejudice"}
              ↓
4. Database lookup → Get book file_path
              ↓
5. Load book text from file (chunked into ~5 min segments)
              ↓
6. TTS synthesizes first chunk → Audio waveform
              ↓
7. Playback engine streams audio to speakers
              ↓
8. User can pause, resume, skip chapters
              ↓
9. Reading position saved in database for resume
```

## Technology Stack

### Backend
- **Framework**: Flask 3.0+
- **Database**: SQLite3
- **TTS**: Coqui TTS 0.22.0
- **STT**: SpeechRecognition 3.10.1
- **Audio**: Pygame 2.5.2
- **Data Processing**: Pandas 1.5.3, NumPy 1.22.0

### Frontend
- **Framework**: React 18+
- **Language**: TypeScript
- **UI Components**: shadcn/ui
- **State Management**: React Hooks

### Infrastructure
- **Containerization**: Docker
- **Web Server**: Gunicorn
- **Reverse Proxy**: Nginx (optional)
- **Version Control**: Git

## Accessibility Features

1. **Voice Control**: All features accessible via voice commands
2. **Screen Reader Compatible**: HTML semantic markup
3. **Keyboard Navigation**: Full keyboard support (Tab, Enter, Arrows)
4. **ARIA Labels**: Proper ARIA attributes for screen readers
5. **Audio Feedback**: All actions provide audio confirmation

## Performance Considerations

### Optimization Strategies

1. **TTS Caching**
   - Cache synthesized audio for books
   - Avoid re-synthesis for repeated chapters

2. **Database Indexing**
   ```sql
   CREATE INDEX idx_book_title ON books(title);
   CREATE INDEX idx_book_author ON books(author);
   ```

3. **Lazy Loading**
   - Load book text in chunks (not all at once)
   - Reduce memory footprint

4. **GPU Acceleration**
   - Use CUDA for TTS if available
   - ~10x faster synthesis on NVIDIA GPUs

### Scalability

**For 100+ Users**:
- Migrate SQLite → PostgreSQL
- Use Redis for caching
- Deploy multiple Flask instances (load balancer)
- Implement session management

```
Load Balancer
     ↓
┌────┴────────────────┐
│                     │
v                     v
Flask 1          Flask 2
  ↓                 ↓
PostgreSQL ←──→ Redis Cache
```

## Security Considerations

1. **API Authentication**: Add JWT tokens for user sessions
2. **CORS**: Configure allowed origins
3. **Input Validation**: Sanitize text input to prevent injection
4. **Rate Limiting**: Prevent abuse of STT/TTS services
5. **HTTPS**: Use SSL/TLS in production
6. **Data Privacy**: Encrypt sensitive user data

## Testing Strategy

### Unit Tests
- Intent classification accuracy
- Search algorithm correctness
- Database operations

### Integration Tests
- Full voice command workflow
- API endpoint responses
- Database interactions

### Accessibility Tests
- Screen reader compatibility
- Keyboard navigation
- Voice command recognition

### Load Tests
- TTS synthesis under load
- Concurrent user sessions
- Database query performance

## Deployment Checklist

- [ ] Set environment variables
- [ ] Initialize database
- [ ] Test TTS model download
- [ ] Configure microphone/speakers
- [ ] Run test suite
- [ ] Set up logging
- [ ] Configure monitoring
- [ ] Document deployment
- [ ] Create backup strategy

---

**Version**: 1.0
**Last Updated**: May 2026
