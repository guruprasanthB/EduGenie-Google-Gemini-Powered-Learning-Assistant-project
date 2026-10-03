# EduGenie AI

EduGenie is a FastAPI-based learning assistant with a browser interface for:

- Asking study questions
- Explaining concepts at different levels
- Creating quizzes from study material
- Summarizing notes
- Generating personalized learning paths

The AI features use the Google Gemini API. The web application and health check can start without an API key, but AI requests need a valid key and an internet connection.

## Requirements

- Python 3.10 or newer (Python 3.11 recommended)
- A Gemini API key for AI responses

## Run on Windows

Open PowerShell in the project folder and run:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `GEMINI_API_KEY` to your own key. Keep this file private; it is excluded from Git and the project ZIP.

Start the application:

```powershell
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000> in a browser. The API documentation is at <http://127.0.0.1:8000/docs>, and the health check is at <http://127.0.0.1:8000/health>.

To stop the server, press `Ctrl+C` in PowerShell.

If PowerShell blocks virtual-environment activation, run the server through the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

## Run the tests

With the environment activated, run:

```powershell
python -m unittest discover -s tests -v
```

## Configuration

Copy `.env.example` to `.env` and edit values as needed:

| Variable | Purpose | Default |
| --- | --- | --- |
| `APP_NAME` | Name shown by the application | `EduGenie AI` |
| `ENVIRONMENT` | Environment label | `development` |
| `GEMINI_API_KEY` | Gemini API key used for AI requests | Empty |
| `GEMINI_MODEL` | Primary Gemini model | `gemini-3.5-flash-lite` |
| `GEMINI_FALLBACK_MODEL` | Model used after a temporary primary-model error | `gemini-3.8-flash` |
| `LOCAL_EXPLANATION_ENABLED` | Allow concept explanations through a local Ollama server | `false` |
| `LOCAL_EXPLANATION_MODEL` | Ollama model for local concept explanations | `llama3.2` |
| `MAX_INPUT_CHARS` | Maximum text accepted by AI features | `20000` |

Local explanations are optional and only apply when Gemini is not configured. To use them, install and start Ollama, download the configured model, and set `LOCAL_EXPLANATION_ENABLED=true` in `.env`. Other AI features still require Gemini.

## Project layout

```text
.
├── app.py                  # Local server entry point
├── main.py                 # FastAPI app and HTTP routes
├── ai_service.py           # Gemini and optional Ollama integration
├── *_module.py             # Learning feature implementations
├── schemas.py              # API request and response models
├── templates/              # Browser interface
├── static/                 # CSS and JavaScript
├── tests/                  # Automated tests
└── phases/                 # Project roadmap details
```

## API endpoints

- `GET /health`
- `POST /qa`
- `POST /explain`
- `POST /quiz`
- `POST /summarize`
- `POST /learn/recommendations`

Request schemas and interactive examples are available at `/docs` while the server is running.

## GitHub and ZIP safety

Do not upload `.env`, API keys, virtual environments, Python cache files, or test caches. `.gitignore` excludes these local files. The handoff ZIP contains the source, tests, documentation, static assets, and templates, but not credentials or generated caches.
