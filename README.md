# InterviewHub (Django Demo)  ![CI](https://github.com/caiobassetti/interview-hub/actions/workflows/ci.yml/badge.svg)

## Architecture
Django 5 + DRF expose a JSON API.
Questions are reusable prompts.
Interviews (Sessions) are sets of questions owned by a facilitator.
Submissions are answers (one participant, one question, one session).
Auth is JWT.
Writes are auth-guarded.

## Quickstart
```bash
# 1) venv + deps
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 2) env + DB + server
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser  # create 'fiona' for demo
python manage.py runserver
```

## Endpoints (core)
- `POST /api/auth/token/` → JWT pair
- `GET/POST /api/questions/` → list/create questions
- `GET /api/questions/<id>/`
- `GET/POST /api/interviews/` → list/create sessions (attach question IDs)
- `GET /api/interviews/<id>/`
- `POST /api/submissions/create/` → submit an answer (binds to logged-in user)
- `GET /api/submissions/` → list user submissions

## Sample cURL
# Token
curl -s -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"fiona","password":"fiona_pw"}'

# Create a scale question (use access token from step 1)
ACCESS="<paste_access_here>"
curl -s -X POST http://127.0.0.1:8000/api/questions/ \
  -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" \
  -d '{"title":"Leadership clarity","qtype":"Scale"}'

## Logging (structured)
Logs are JSON via structlog; example line:
{"event":"submit_answer","level":"info","interview":20,"question":11,"user":"alice","answer":"4","timestamp":"2025-09-23T09:30:00Z"}

## CI/CD
GitHub Actions workflow (.github/workflows/ci.yml) runs `ruff` + `pytest` on every push/PR:
**Current status: passing.**

## Repo layout

```
interview-hub/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions: ruff + pytest
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py                 # Shared settings (DB, apps, logging, DRF)
│   │   ├── dev.py                  # Dev overrides (DEBUG=True)
│   │   ├── prod.py                 # Prod overrides (DEBUG=False)
│   │   └── test.py                 # Test overrides
│   ├── asgi.py
│   ├── urls.py                     # Routes: /api/... endpoints
│   └── wsgi.py
├── interviewhub/
│   ├── __init__.py
│   ├── admin.py                    # Django admin registers
│   ├── apps.py
│   ├── models.py                   # Question, Interview, Submission
│   ├── serializers.py              # Serializers for API
│   ├── urls.py                     # API routes
│   └── views.py                    # DRF views
├── tests/
│   └── test_flow.py                # End-to-end flow test (create -> submit -> summarize)
├── .env.example                    # Sample env vars
├── manage.py                       # Django entrypoint
├── pyproject.toml                  # Ruff config (Used in CI)
├── pytest.ini                      # Pytest config
├── requirements.txt                # Dependencies: Django, DRF, structlog, pytest, etc.
└── README.md                       # Run steps, endpoints, architecture, cURL, CI badge
```
