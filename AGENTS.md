# AGENTS.md

## Scope

These instructions apply to the entire repository unless a more specific `AGENTS.md`
is added deeper in the tree.

## General workflow

- Never commit failing code. Run and document the relevant backend (`pytest`) or
  frontend (`npm run check && npm run test`) suites when you touch those areas.
- Keep diffs minimal: don’t reformat untouched files and avoid sweeping refactors
  unless the task demands it.
- Write descriptive commit messages (“area: summary”) and keep PR titles succinct.
- Prefer small, focused PRs. If a change spans both backend and frontend, describe
  the cross-service impact in the PR body.

## Backend (`backend/`)

- Target Python 3.13+. Match the existing FastAPI + SQLAlchemy async style.
- Always add or update type hints; favor `Annotated`/`TypedDict` where clarity helps.
- Keep functions pure where possible; push I/O to service layers.
- Log through the existing `logging` module; no `print`.
- Database migrations live under `backend/alembic`. Every schema change requires
  a migration plus corresponding SQLAlchemy model updates.
- Tests belong in `backend/tests/` and should mock external services (OpenAI, RSS)
  via the provided fixtures.
- Whenever possible, use the latest versions of packages, i.e., the latest openai
  library instead of legacy versions.

## Frontend (`frontend/`)

- This is a SvelteKit + TypeScript app. Use TypeScript for all new code and export
  shared types from `src/lib`.
- Favor Svelte stores and derived values instead of manual event emitters.
- Keep API calls centralized in `src/lib/api.ts`; component files should not hit
  `fetch` directly.
- Run `npm run lint` and `npm run check` when touching Svelte/TS files.
- CSS lives alongside components using `<style lang="postcss">`; keep styles scoped.
- Whenever possible, use the latest versions of node packages, i.e., the latest svelte
  library instead of legacy versions.

## DevOps / configs

- Dockerfiles must stay multi-stage and slim; install only runtime deps in the
  final image.
- Environment variables documented in `README.md` must remain the single source of
  truth; update the README if you add or change any.
- When editing `docker-compose.yml`, ensure services continue to boot with the
  default `.env.example` values.

## Documentation

- Any new feature or breaking change requires README (or relevant doc) updates.
- Inline code comments should explain “why”, not “what”; favor module docstrings
  for high-level context.

## PR message (for `make_pr`)

- Title: “area: concise summary” (e.g., `backend: fix story scheduler jitter`).
- Body:
  1. Summary bullet list of changes.
  2. Testing section enumerating the commands you ran and their results.
