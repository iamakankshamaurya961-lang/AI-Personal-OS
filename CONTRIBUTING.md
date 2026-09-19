# Contributing to AI Personal OS

Thank you for your interest in contributing! Here's how to get started.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/iamakankshamaurya961-lang/AI-Personal-OS.git
   cd AI-Personal-OS
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dev dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Install and start Ollama:**
   ```bash
   ollama serve
   ollama pull llama3
   ```

## Running the Application

```bash
# Start backend
uvicorn backend.main:app --reload

# Start frontend (in a new terminal)
python3 -m http.server 5500 --directory frontend
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=backend --cov-report=term-missing
```

## Code Quality

```bash
# Lint check
ruff check backend/

# Auto-fix lint issues
ruff check backend/ --fix
```

## Environment Configuration

Copy `.env.example` to `.env` and customize:
```bash
cp .env.example .env
```

## Coding Standards

- Use **type hints** on all function signatures
- Write **docstrings** for all public methods
- Use `logging` instead of `print()` for debug output
- Wrap database connections in `try/finally` blocks
- Add tests for any new features

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass and lint is clean
5. Commit with clear messages (`git commit -m 'Add: amazing feature'`)
6. Push and open a Pull Request

## Security

- **Never commit** API keys, OAuth credentials, or access tokens
- Store secrets in `.env` (excluded from git)
- Sanitize file uploads with `os.path.basename()`
