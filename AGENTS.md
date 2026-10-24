# AGENTS.md

Rules for every AI coding agent (and human) working in this repo. Several people's agents push here at the same time, so follow these to avoid clobbering each other's work.

## Workflow

1. **Pull before starting.** Always start from the latest `main`:
   ```bash
   git checkout main
   git pull origin main
   ```
2. **One branch per task.** Create a fresh branch for each task. Never reuse a branch for unrelated work.
   ```bash
   git checkout -b <your-name>/<short-task-description>
   # e.g. tarun/add-login-page
   ```
3. **Never push to `main`.** All changes go through a pull request. Never force-push to `main`. The author may merge their own PR after checking it; reviews are optional.
4. **Keep PRs small.** One logical change per PR — aim for a diff someone can review in a few minutes. Split large features into several PRs.
5. **Sync before opening/updating a PR.** If `main` has moved, rebase or merge it into your branch and fix conflicts locally:
   ```bash
   git fetch origin
   git rebase origin/main   # or: git merge origin/main
   ```
6. **Open a PR using the template** in `.github/pull_request_template.md` and fill in every section.

## Project conventions

- Backend: Python 3.12 + FastAPI in `backend/`. Add API routes under the `/api` prefix in `backend/app/` and tests in `backend/tests/`.
- Frontend: plain HTML/CSS/JS in `frontend/` (no build step), served by the backend at `/`. Call the backend with `fetch("/api/...")`.
- Add new Python dependencies to `backend/requirements.txt` (dev-only ones to `requirements-dev.txt`) with pinned versions.
- Before pushing, run from `backend/`: `ruff format . && ruff check . && pytest`. CI runs the same checks.

## Data format (`data/`)

The app maps sea turtle migrations over time. All data lives in `data/` as plain JSON — the only copy; don't add duplicates under `frontend/`. The backend serves it via `/api/species`, `/api/migrations` (filters: `from`, `to`, `species`, `ocean`, `depth`) and `/api/oceans`, and the raw files at `/data/*`. Keep these shapes stable; if you must change them, update `backend/tests/test_data.py` and tell the team.

- `data/species.json` — array of the 7 species: `id` (slug, e.g. `loggerhead`), `common_name`, `scientific_name`, `color` (hex, used for map lines), `depth_range_m: {typical_max, record_max}`, `iucn_status`, `blurb`, `sources: [{title, url}]`, `dive_profile` (array of `{t, depth_m}` points, t from 0 to 1, shaping the dive chart; illustrative until the data team verifies).
- `data/migrations.geojson` — GeoJSON `FeatureCollection` of `LineString` routes (coordinates are `[lon, lat]`). Each feature's `properties`: `id`, `species` (a species `id`), `name`, `ocean` (an ocean `id`), `life_stage`, `start`/`end` (ISO dates — the years the route is known to be active), `months` (1–12, when the migration happens each year), `depth_m: {min, max}`, `confidence` (`documented` or `illustrative`), `notes`, `sources`.
- `data/oceans.json` — array of `id`, `name`, `bbox` `[minLon, minLat, maxLon, maxLat]` (Pacific crosses the antimeridian, so minLon > maxLon), `center` `[lon, lat]`.

Time filtering rule: a route is shown for a selected time window if its `start`–`end` span overlaps the window **and** at least one of its `months` falls inside the window.

## Do

- Read `README.md`, this file, and `CONTRIBUTING.md` before making changes.
- Make focused edits; match the existing code style.
- Run any tests, linters, and builds the repo has before pushing.
- Describe *what* changed and *why* in the PR description.
- Use clear commit messages (e.g. `Add login form validation`).

## Don't

- Don't push directly to `main` or force-push shared branches.
- Don't commit secrets, API keys, `.env` files, or credentials.
- Don't make sweeping refactors, reformat unrelated files, or rename things outside your task.
- Don't delete or rewrite other people's work without asking in the PR.
- Don't commit generated files, build output, or large binaries unless the repo already does.

## If something goes wrong

- Merge conflict you're unsure about: stop and ask the PR author / team instead of guessing.
- Accidentally committed to `main` locally: move the commit to a new branch (`git branch my-fix && git reset --hard origin/main`) before pushing.
