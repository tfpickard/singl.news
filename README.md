# Singl News

Singl News is a two-service project that publishes a single, continuously evolving
news narrative assembled from multiple RSS feeds. The backend service ingests feed
items, prompts OpenAI to extend the forever story, and exposes REST plus WebSocket
APIs. The SvelteKit frontend doomscrolls through the current narrative and history.

## Repository structure

```
backend/   FastAPI service, scheduler, and database migrations
frontend/  SvelteKit doomscroll experience
```

## Running locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Environment variables:

- `DATABASE_URL` – SQLAlchemy URL (defaults to local SQLite file)
- `OPENAI_API_KEY` – optional; without it a deterministic fallback story is used
- `SINGL_FEEDS` – comma-separated RSS URLs
- `SINGL_UPDATE_MINUTES` – scheduler interval

Copy `.env.example` to `.env` and adjust any values you need before starting the
backend. The service automatically loads variables from that file on startup.

Run tests with:

```bash
pytest
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE` and `VITE_WS_BASE` to point at the backend if not using the
defaults (`http://localhost:8000/api` and `ws://localhost:8000/ws/story`).

### Docker

The project ships with a compose setup that launches Postgres, the backend, and the
frontend together.

```bash
docker compose up --build
```

The frontend will be reachable at http://localhost:4173 and proxies API/WebSocket
calls to the backend service.
