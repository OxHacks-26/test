# OxHack '26 

**Topic of Time**

Time is the subject. A row of numbers does not say what to do; the sequence does. This project reads how something has changed over time, predicts the next stretch, and turns that into a decision: act now, wait, or look closer.

The screen is built around that moment of choice. Recent history stays visible, the prediction sits on the same timeline, and the recommendation names the reason it was made. Moving the inputs moves the forecast and the decision together, so the timing is something you can see rather than a score buried in a table.

## Open it

The screen is the Turtle Tide app in `ui/`. It needs Python, so GitHub cannot host it as a static page. From the GitHub repo, use Codespaces: the dev container installs dependencies, starts the app, and opens port 8080 in your browser.

[Open Turtle Tide in GitHub Codespaces](https://codespaces.new/OxHacks-26/turtle-tide?quickstart=1)

A judge needs a GitHub account. The first open installs the Python packages, so give it a few minutes. When the Codespace is ready, open the **Ports** panel and click the globe next to **Turtle Tide** (port 8080). That opens the site in your browser. Click **Start exploring**. The sample years are 2006, 2010, 2015, and 2020.

A Codespace stops after it sits idle, and the old browser tab then says the site cannot be reached. Open the Codespace again and use the Ports globe. Do not open `http://127.0.0.1:8080` from the README in your own browser: that address is inside the Codespace, not on your computer. If the terminal says the address is already in use, the app is already running and the Ports globe is the way in.

That Codespaces link is the link to submit. It uses the default branch, so this setup has to be on `main`. GitHub cannot keep one always-on website for this Python app.

On your own machine, from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements-dev.txt
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Open http://127.0.0.1:8080. That page is the whole Turtle Tide screen: the header, ocean buttons, and time controls, with the map inside the atlas. The map file alone is at http://127.0.0.1:8080/map/. API routes live under `/api`.
