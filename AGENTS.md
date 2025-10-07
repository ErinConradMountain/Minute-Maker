# Repository Guidelines

This guide helps contributors work efficiently in this repository.

## Project Structure & Module Organization
- `src/` — application/source code grouped by feature.
- `tests/` — automated tests mirroring `src/` (e.g., `tests/utils/…`).
- `assets/` — static files (images, templates, example data).
- `scripts/` — helper scripts for build, lint, and release.
- `dist/` — build artifacts (generated; do not edit).

## Build, Test, and Development Commands
- `npm run dev` or `python -m src` — run the app locally for development.
- `npm run build` or `python setup.py sdist bdist_wheel` — produce artifacts in `dist/`.
- `npm test` or `pytest -q` — run unit tests.
- `npm run lint` or `ruff check .` — lint/format check.

## Coding Style & Naming Conventions
- Indentation: 2 spaces (JS/TS), 4 spaces (Python).
- Filenames: `kebab-case` for web assets, `snake_case.py` for Python, `camelCase` for small JS utilities; classes use `PascalCase`.
- Keep modules focused with small, single‑purpose functions.
- Run formatters before commits: `prettier --write .` (web) or `ruff format .` (python).

## Testing Guidelines
- Frameworks: Jest (JS/TS) or Pytest (Python).
- Mirror `src/` paths in `tests/` (e.g., `src/utils/time.ts` → `tests/utils/time.test.ts`).
- Aim for ≥80% line coverage on changed code: `npm run test:coverage` or `pytest --cov=src`.
- Use descriptive test names; one behavior per test.

## Commit & Pull Request Guidelines
- Commits: Conventional style when possible (e.g., `feat: add agenda export`, `fix: handle empty input`). Keep scope small; write imperative, present‑tense messages.
- PRs: include a clear summary, linked issue (e.g., `Closes #123`), screenshots for UI changes, and test evidence (commands/output or coverage). Ensure CI (lint, tests) passes before review.

## Security & Configuration Tips
- Never commit secrets; use environment variables in `.env.local` (git‑ignored).
- Validate all user input; centralize time/date parsing in a single utility.

## AI Providers: Qwen & Whisper
- Env files: copy `.env.example` → `.env.local` and fill values.
- Qwen env:
  - `QWEN_API_KEY` (required)
  - `QWEN_API_ENDPOINT` (model name like `qwen/qwen2.5-vl-72b-instruct:free` or a full URL)
  - Check: `PYTHONPATH=$PWD python scripts/check_qwen.py`
- Whisper env:
  - `WHISPER_API_KEY` (or reuse `OPENAI_API_KEY`)
  - `WHISPER_API_ENDPOINT` (full base URL if required)
  - Generate sample audio: `python scripts/gen_sample_audio.py assets/sample.wav`
  - Check: `PYTHONPATH=$PWD python scripts/check_whisper.py assets/sample.wav`
- OpenAI‑compatible mapping: scripts auto‑map `QWEN_*`/`WHISPER_*` → `OPENAI_*` when needed.

## Dev Environment Quickstart
- Install dev deps: `python -m pip install -r requirements-dev.txt`
- Run tests with coverage: `PYTHONPATH=$PWD pytest -q`
- Optional: install OpenAI client for live checks: `python -m pip install openai`
- PowerShell helper: `./scripts/dev.ps1 -Task init|test|qwen|whisper|all` (uses `.venv`, installs deps, runs checks; add `-Audio assets/sample.wav` to choose audio path)

## Agent‑Specific Instructions
- Respect this guide across the repo tree.
- Keep changes minimal and focused; update docs/tests alongside code.

