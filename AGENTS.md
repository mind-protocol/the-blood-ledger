# Repository Guidelines

## Project Structure & Module Organization
- `engine/` contains the FastAPI backend, domain modules (`history/`, `graph/`, `mechanisms/`), and runnable scripts (`run.py`, `bin/`). Read the matching chain in `docs/` before touching any module.
- `frontend/` is a Next.js 16 + TypeScript app (`app/`, `components/`, `hooks/`, `public/`); ship static art to `public/` and gameplay captures to `screenshots/`.
- `falkordb-browser/` runs the schema inspector, while `data/`, `prompts/`, and `scenarios/` feed the narrative graph. Agent briefs live in `agents/`—sync work back into `.context-protocol/state/`.

## Build, Test, and Development Commands
- `docker start falkordb` (or the init recipe in `README.md`) boots the shared FalkorDB instance on `6379`; UI sits at `http://localhost:3002`.
- `cd engine && python3 run.py --reload` serves the API; prepend `PYTHONPATH=.` for tooling calls like `python3 -m engine.history.cli list`.
- `cd engine && pytest tests` runs the suite. Use `-m "not integration"` to skip FalkorDB cases or `-k moment` for targeted runs.
- `cd frontend && npm run dev` starts the UI, `npm run build` performs the prod check, and `npm run lint` enforces ESLint/Tailwind.
- `cd falkordb-browser && PORT=3001 npm run dev` spins up the standalone inspector if you need a separate schema window.

## Coding Style & Naming Conventions
- Python: 4-space indent, rich type hints, docstrings that state intent, and `snake_case` names. Persist structured data in YAML under `docs/`/`data/` and prefer Pydantic for IO.
- Frontend: Strict TypeScript, PascalCase components, camelCase hooks/utilities, Tailwind 4 for styling. Keep helper modules colocated, run `npm run lint` before pushing, and reference `eslint.config.mjs` for rule exceptions.

## Testing Guidelines
- Backend tests stay in `engine/tests/` (e.g., `test_history.py`). Mirror new modules with `test_<module>.py`, tag FalkorDB work with `@pytest.mark.integration`, and leverage temp dirs/fixtures for file IO.
- Frontend component tests (React Testing Library or Playwright) should sit beside the component (`components/FacesPanel/FacesPanel.test.tsx`) and run through your chosen runner even though no npm script exists yet.
- Graph or `.context-protocol` changes require updated docs plus a reproducible verification command in the PR (e.g., `python3 -m engine.graph.sync --dry-run`).

## Commit & Pull Request Guidelines
- Commits follow short, imperative subjects with optional scopes (`engine: tighten timestamp parsing`, `frontend: add ledger hint`). Include why + follow-up work in the body.
- PRs must summarize player-facing impact, list services touched, cite commands/tests executed, and attach evidence (screenshots, log excerpts). Link scenario IDs and sync notes whenever `.context-protocol` artifacts move so downstream agents can trace rationale.
