# Module 11 — Core Skills Drill: Instrument a Toy FastAPI Service

Add three middlewares (request-id, structured logging, metrics), three
Prometheus metric families (counter, histogram, gauge), and mount
`/metrics` on a two-endpoint toy FastAPI app. Verify with a self-test
suite you author in `tests/test_drill.py`.

The published Drill page is the canonical task list. See
TalentLMS → Module 11 → Drill 11 for the link.

## What ships here

```
.
├── app.py                          TODO: metric declarations + middlewares + /metrics mount
├── tests/
│   ├── test_drill.py               YOUR self-tests go here (pytest.fail placeholders)
│   ├── test_drill_autograde.py     autograder (do not modify)
│   └── conftest.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Setup

Use **Python 3.11** for this template (the pinned `pydantic==2.6.0` does not build on Python 3.13).

```bash
python3.11 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the autograder locally

```bash
pytest tests/ -v
```

On the unmodified starter, the autograder will FAIL (by design — the
metric declarations, middlewares, and `/metrics` mount are all TODOs,
and your `tests/test_drill.py` is full of `pytest.fail` placeholders).

## Submission (fork-and-submit)

You created the `drill-11-instrument-toy-service` branch during Setup. From that branch:

```bash
git add -A
git commit -m "Drill 11 — instrument toy service"
git push -u origin drill-11-instrument-toy-service
```

Open a PR within your fork. The PR description must include:

1. Confirmation that `pytest tests/ -v` passes locally.
2. The first 20 lines of your `/metrics` output (`uvicorn app:app --port 8001 &` → make a few calls → `curl -L localhost:8001/metrics | head -20`). The `-L` follows the 307 redirect Starlette serves on the mounted `/metrics`.
3. Paste your PR URL into TalentLMS → Module 11 → Drill 11 to submit this assignment.

---

## License

This repository is provided for educational use only. See [LICENSE](LICENSE) for terms.

You may clone and modify this repository for personal learning and practice, and reference code you wrote here in your professional portfolio. Redistribution outside this course is not permitted.
