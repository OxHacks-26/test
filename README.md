# OxHack '26 

**Topic of Time**

Time is the subject. A row of numbers does not say what to do; the sequence does. This project reads how something has changed over time, predicts the next stretch, and turns that into a decision: act now, wait, or look closer.

The screen is built around that moment of choice. Recent history stays visible, the prediction sits on the same timeline, and the recommendation names the reason it was made. Moving the inputs moves the forecast and the decision together, so the timing is something you can see rather than a score buried in a table.

## Run

Requires Python 3.12.

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000. API routes live under `/api`.
