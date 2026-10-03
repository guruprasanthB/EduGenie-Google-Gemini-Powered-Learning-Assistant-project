# EduGenie AI — Phase-wise Project Document

## Project overview

EduGenie AI is a web-based learning assistant. It provides question answering, concept explanations, quiz generation, text summarization, and personalized learning-path recommendations through a FastAPI backend and browser interface.

## Phase summary

| Phase | Focus | Current status |
| --- | --- | --- |
| 1 | Core AI learning assistant | Implemented baseline |
| 2 | User experience and interface | Implemented baseline |
| 3 | Personalization and progress tracking | Planned |
| 4 | Production, monitoring, and scale | Planned |

“Implemented baseline” means the corresponding core functionality exists in the current project. It does not imply production deployment or that every future enhancement is complete.

---

## Phase 1 — Core AI Learning Assistant

### Objective

Build the backend features that let learners ask questions, study concepts, create quizzes, summarize notes, and plan what to learn next.

### Implemented scope

- FastAPI application and health endpoint
- Gemini-backed AI service, with configurable model and fallback model
- Question-answering endpoint
- Concept-explanation endpoint
- Quiz-generation endpoint
- Text-summarization endpoint
- Learning-path recommendation endpoint
- Request validation and user-facing error handling
- Automated tests for routes, provider errors, and quiz response parsing

### Main project files

- `main.py` — API routes and application setup
- `ai_service.py` — AI provider requests and response handling
- `schemas.py` — Request and error models
- `qna.py`, `explanation_module.py`, `quiz_module.py`, `summary_module.py`, `learning_path.py` — Learning features
- `tests/` — Automated tests

### Remaining improvement ideas

1. Expand automated test coverage for malformed provider responses and boundary inputs.
2. Add structured logging for provider failures and request diagnostics.
3. Validate provider behavior against the currently configured Gemini model and API.

### Success criteria

- Each learning endpoint accepts valid input and returns its documented result.
- Invalid input and provider failures produce clear errors.
- The app can start locally without an AI key; AI features report configuration issues clearly.

---

## Phase 2 — User Experience and Interface

### Objective

Make the learning features usable through a straightforward, responsive browser interface.

### Implemented scope

- Study desk homepage with tabs for each learning feature
- Forms whose fields adapt to the selected tool
- Asynchronous requests to the FastAPI endpoints
- Loading and error feedback
- Results display, copy action, and clear action
- Responsive styling for desktop and mobile layouts
- Health indicator for application/AI-key status

### Main project files

- `templates/index.html` — Page structure
- `static/css/style.css` — Interface styles
- `static/css/js/app.js` — Tab, form, API, and result interactions

### Remaining improvement ideas

1. Test keyboard navigation and screen-reader behavior.
2. Review the interface on common mobile screen sizes.
3. Add browser-level tests for the main user journeys.

### Success criteria

- Learners can access all five study tools from the interface.
- Requests show clear loading, success, and error states.
- The layout and controls remain usable on mobile and desktop.

---

## Phase 3 — Personalization and Progress Tracking

### Objective

Make EduGenie more adaptive by remembering learning context and using it to guide future study.

### Planned deliverables

- User profiles or private learning sessions
- Saved questions, summaries, quiz results, notes, and learning paths
- Progress and completion tracking
- Difficulty adaptation based on learner level and results
- Topic history and recommendations informed by prior activity

### Planned tasks

1. Define the user/session model and privacy requirements.
2. Choose and implement persistent storage for profiles and learning records.
3. Add user controls to view, save, and delete learning history.
4. Adapt explanations and recommendations to learner preferences and progress.
5. Track meaningful metrics such as completed topics and learning streaks.
6. Add tests for persistence, access boundaries, and personalized behavior.

### Success criteria

- A learner can revisit saved work and resume a learning path.
- Recommendations use relevant learner context and remain understandable.
- Personal data is protected and can be managed by the user.

---

## Phase 4 — Production, Monitoring, and Scale

### Objective

Prepare the application for dependable deployment and operation beyond a local development environment.

### Planned deliverables

- Production configuration and deployment instructions
- Secure secrets management
- Monitoring, structured logs, and error reporting
- Rate limits and usage controls
- Resilient AI-provider handling
- CI checks and deployment validation
- Documented scaling and backup strategy

### Planned tasks

1. Select a hosting platform and define development, staging, and production environments.
2. Configure secrets outside source control and verify they are not exposed in logs.
3. Add structured application logs, metrics, and actionable health checks.
4. Set request limits, timeouts, and safe handling for provider quotas and outages.
5. Add automated build/test checks and deployment validation.
6. Document operational procedures, backups, and scaling limits.

### Success criteria

- The app can be deployed repeatably without committing secrets.
- Operators can detect and diagnose service and provider failures.
- Usage and resource consumption have explicit safeguards.
- Releases are validated by automated checks.

---

## Suggested implementation order

1. Complete the remaining tests and provider compatibility checks in Phase 1.
2. Validate accessibility, responsive behavior, and browser flows in Phase 2.
3. Decide privacy, account, and data-retention requirements before implementing Phase 3 storage.
4. Choose a hosting target and operational requirements before finalizing Phase 4 deployment work.

## How to run locally

From the project directory, install dependencies and start the development server:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` in a browser. AI-powered features require a valid `GEMINI_API_KEY` in the local `.env` file.
