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

The app maps sea turtle migrations over time. All data lives in `data/` as plain JSON so the backend can serve it and the frontend can draw it. Keep these shapes stable; if you must change them, update `backend/tests/test_data.py` and tell the team.

- `data/species.json` — object with a `species` array of the 7 species: `id`, `common_name`, `scientific_name`, `colour`, `depth_range_m: {min, max}`, `facts` (short strings), `source_ids`. `GET /api/species` returns that array plus `textboxes` for the depth panel and `depth_marks` for where to draw the turtle. Diet and food fields are not served.
- `data/textboxes.json` — three sourced textboxes per species (`Habitat`, `Population and extinction risk`, `Life expectancy`), shown when that species is clicked.
- `data/migrations.geojson` — GeoJSON `FeatureCollection` of illustrative `LineString` routes. There is one sample route per species for 2006, 2010, 2015, and 2020. Each feature's `properties` include `species_id`, `route_id`, `year`, `ocean`, `dates` (ISO timestamps, one per position), `months`, and `depth_m` (parallel to the positions). `GET /api/migrations` accepts `year` as that whole calendar year.
- `data/animation_sightings.json` and `data/animation_species_predictions.json` — two example positions per species per year, taken from those routes, plus a year status for every species. `GET /api/years` returns the years. `GET /api/predictions` returns the positions with coordinates. `species` and `year` each limit the rows.
- `data/oceans.json` — array of `id`, `name`, `bbox` `[minLon, minLat, maxLon, maxLat]` (Pacific crosses the antimeridian, so minLon > maxLon), `center` `[lon, lat]`.

Time filtering rule: a route is shown for a selected time window when one of its dated positions falls inside the window **and** that position's month falls inside the window. Routes that only have `start`/`end` match when that span overlaps the window and at least one listed month falls inside it.

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
