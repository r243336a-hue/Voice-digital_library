# Contributing to Voice-Navigable Digital Library

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🎯 Before You Start

- Read the [README.md](README.md) to understand the project
- Review the [SETUP.md](SETUP.md) for development setup
- Check the [ARCHITECTURE.md](ARCHITECTURE.md) to understand system design

## 📋 How to Contribute

### 1. Report Bugs

Found a bug? Open an issue with:
- **Title**: Clear description of the bug
- **Environment**: OS, Python version, Browser
- **Steps to Reproduce**: Detailed steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happened
- **Screenshots/Logs**: If applicable

```markdown
## Bug Report

**Environment:**
- OS: Windows 10
- Python: 3.10.5
- Browser: Chrome 115

**Steps to Reproduce:**
1. Click on search bar
2. Speak "find pride"
3. Expected result: Shows matching books

**Actual Result:**
Error message appears instead

**Logs:**
```
[error] STT failed: ...
```
```

### 2. Suggest Features

Want a new feature? Open an issue with:
- **Title**: Feature description
- **Use Case**: Why would this help users
- **Proposed Solution**: How you'd implement it
- **Alternatives**: Other approaches considered

```markdown
## Feature Request

**Title:** Add bookmark functionality

**Use Case:**
Users want to save favorite passages for quick access

**Proposed Solution:**
- Add "bookmark" button in playback controls
- Store bookmarks in database
- Show bookmark list in sidebar

**Alternatives:**
- Just save reading position (already done)
- Cloud sync bookmarks
```

### 3. Submit Code Changes

#### Fork and Clone
```bash
git clone https://github.com/YOUR-USERNAME/Voice-digital_library.git
cd Voice-digital_library
git remote add upstream https://github.com/r243336a-hue/Voice-digital_library.git
```

#### Create a Feature Branch
```bash
git checkout -b feature/my-feature
# or
git checkout -b fix/my-bug-fix
```

#### Make Your Changes

Follow these conventions:

**Python Code Style:**
- Use PEP 8 (enforced by `black`)
- Run `black backend/` before committing
- Add docstrings to functions:

```python
def search_books(query: str, limit: int = 10) -> List[Dict]:
    """
    Search for books by title or author.
    
    Args:
        query: Search query string
        limit: Maximum results to return (default: 10)
        
    Returns:
        List of book dictionaries with id, title, author
        
    Raises:
        ValueError: If query is empty
    """
```

**TypeScript Code Style:**
- Use ESLint configuration
- Add type annotations:

```typescript
interface Book {
  id: number;
  title: string;
  author: string;
}

const searchBooks = async (query: string): Promise<Book[]> => {
  // Implementation
};
```

**Git Commits:**
- Use clear, descriptive commit messages
- Reference issues: `Fix #123`

```bash
git add .
git commit -m "feat(search): add fuzzy matching for book titles

- Implement Levenshtein distance algorithm
- Handle typos in search queries
- Add tests for edge cases

Closes #42"
```

#### Run Tests
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=backend tests/

# Check code style
black --check backend/
flake8 backend/
```

#### Push Your Branch
```bash
git push origin feature/my-feature
```

#### Create a Pull Request

Go to GitHub and create a PR with:
- **Title**: Clear description of changes
- **Description**: What changed and why
- **References**: Related issues (closes #123)
- **Testing**: How you tested the changes
- **Screenshots**: If applicable

```markdown
## PR Description

**What:** Add fuzzy search for book titles
**Why:** Users make typos, fuzzy matching handles this

**Changes:**
- Added `fuzzy_search()` function in search.py
- Implemented Levenshtein distance algorithm
- Added 10 unit tests

**Testing:**
- Ran `pytest tests/test_search.py -v`
- Tested with common typos: "prde and prejdice"
- Manual testing in frontend

**Screenshots:**
[Before/After images if UI changed]

Closes #42
```

## 📐 Code Standards

### Python

**Imports:**
```python
# Standard library
import os
from pathlib import Path

# Third-party
import flask
import numpy as np

# Local
from backend.db_utils import get_book
```

**Type Hints:**
```python
from typing import List, Dict, Optional, Tuple

def process_text(text: str, max_length: int = 1000) -> str:
    """Process and clean text."""
    pass

def search(query: str) -> List[Dict[str, any]]:
    """Search for books."""
    pass
```

**Error Handling:**
```python
try:
    result = tts.tts(text=large_text)
except ValueError as e:
    logger.error(f"TTS failed: {e}")
    raise
```

### TypeScript

**Interfaces:**
```typescript
interface Book {
  id: number;
  title: string;
  author: string;
  filePath: string;
}

interface SearchResult {
  books: Book[];
  totalCount: number;
  query: string;
}
```

**Components:**
```typescript
interface BookCardProps {
  book: Book;
  onPlay: (bookId: number) => void;
  onBookmark: (bookId: number) => void;
}

const BookCard: React.FC<BookCardProps> = ({ book, onPlay, onBookmark }) => {
  return <div>{/* Component JSX */}</div>;
};
```

## 🧪 Testing Requirements

- **Unit Tests**: Test individual functions
- **Integration Tests**: Test component interactions
- **Accessibility Tests**: Ensure keyboard/screen reader support

```python
# Example test
def test_search_with_fuzzy_matching():
    """Test fuzzy search handles typos."""
    results = search_books("pridde and prejudice")
    assert len(results) > 0
    assert results[0]['title'] == "Pride and Prejudice"

def test_search_empty_query():
    """Test search with empty query."""
    with pytest.raises(ValueError):
        search_books("")
```

## 📝 Documentation

- Update README if adding features
- Add docstrings to all functions
- Comment complex logic
- Update ARCHITECTURE.md if changing system design

## 🔄 Review Process

1. **Automated Checks**: Tests must pass
2. **Code Review**: Maintainers review code
3. **Feedback**: Address requested changes
4. **Approval**: Need 1+ approvals
5. **Merge**: PR is merged to main

## 📌 Checklist Before Submitting PR

- [ ] Code follows PEP 8 / ESLint style
- [ ] Added/updated tests
- [ ] Tests pass: `pytest tests/`
- [ ] No new warnings/errors
- [ ] Updated documentation
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

## 🎓 Development Tips

### Quick Start
```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

# Run with hot reload
FLASK_ENV=development FLASK_DEBUG=1 python backend/app.py

# Watch tests
pytest-watch tests/

# Format code
black backend/ && isort backend/
```

### Debugging
```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use debugger
import debugpy
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()
```

### Database Debugging
```bash
# Open SQLite shell
sqlite3 data/database/library.db

# Check tables
.tables

# Query books
SELECT * FROM books;
```

## 🆘 Need Help?

- Check [Discussions](https://github.com/r243336a-hue/Voice-digital_library/discussions)
- Comment on related [Issues](https://github.com/r243336a-hue/Voice-digital_library/issues)
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Review existing code for patterns

## 📜 License

By contributing, you agree that your contributions are licensed under the Apache License 2.0.

## 🙏 Thank You!

Your contributions help make this tool more accessible for visually impaired users. We appreciate your effort!

---

**Questions?** Open a discussion or issue!
