# OxHack '26 

**Topic of Time**

Time is the subject. A row of numbers does not say what to do; the sequence does. This project reads how something has changed over time, predicts the next stretch, and turns that into a decision: act now, wait, or look closer.

The screen is built around that moment of choice. Recent history stays visible, the prediction sits on the same timeline, and the recommendation names the reason it was made. Moving the inputs moves the forecast and the decision together, so the timing is something you can see rather than a score buried in a table.

## Open it

The screen is the Turtle Tide app in `ui/`. It needs Python, so GitHub cannot host it as a static page. From the GitHub repo, use Codespaces: the dev container installs dependencies, starts the app, and opens port 8080 in your browser.

[Open Turtle Tide in GitHub Codespaces](https://codespaces.new/OxHacks-26/test?quickstart=1)

A judge needs a GitHub account. The first open installs the Python packages, so give it a few minutes. A browser tab then opens Turtle Tide on port 8080. If it does not, open the Ports panel and choose Turtle Tide. Click **Start exploring**. The sample years are 2006, 2010, 2015, and 2020.

That Codespaces link is the link to submit. It uses the default branch, so this setup has to be on `main`. GitHub cannot keep one always-on website for this Python app.

On your own machine:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt -r ui/requirements.txt
cd ui && python3 app.py
```

Then open http://127.0.0.1:8080. The process prints that address and does not launch a browser itself.

The API and the map page alone still run from `backend/`:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000. API routes live under `/api`.
