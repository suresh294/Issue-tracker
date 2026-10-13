# Issue Tracker API

[![CI](https://github.com/suresh294/Issue-tracker/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/suresh294/Issue-tracker/actions/workflows/ci.yml)

A FastAPI and PostgreSQL backend prototype for issue management. It demonstrates CRUD operations, optimistic version checks, comments, labels, bulk status updates, CSV import, and aggregate reports.

> **Deployment status:** A public deployment URL has not been verified. This API is intended for local development and is not production-ready; authentication and authorization are not implemented.

## Features

- Create, list, and retrieve issues.
- Update issue titles with optimistic concurrency control using a version field.
- Add comments with non-empty body validation.
- Replace issue labels.
- Bulk-update issue status.
- Import issues from CSV.
- Report top assignees and average resolution time.

## Technology Stack

- Python
- FastAPI and Uvicorn
- SQLAlchemy
- PostgreSQL (`psycopg2-binary`)
- pandas for CSV import

## Prerequisites

- Python 3.10 or newer
- PostgreSQL
- pip

## Local Setup

From the repository root:

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install dependencies and configure the database:

```bash
pip install -r requirements.txt
cp .env.example .env
```

On Windows PowerShell, use `Copy-Item .env.example .env`. Edit `.env` and set `DATABASE_URL` to your PostgreSQL connection string. Create the database named in that URL before starting the app.

Start the API:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API Overview

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/issues` | Create an issue |
| GET | `/issues` | List issues |
| GET | `/issues/{id}` | Get an issue |
| PATCH | `/issues/{id}` | Update title using a version check |
| POST | `/issues/{id}/comments` | Add a comment |
| PUT | `/issues/{id}/labels` | Replace issue labels |
| POST | `/issues/bulk-status` | Bulk status update |
| POST | `/issues/import` | Import issue rows from CSV |
| GET | `/reports/top-assignees` | Aggregate issues by assignee |
| GET | `/reports/latency` | Average time to resolution |

## Security and Known Limitations

- No authentication or authorization middleware is implemented.
- Database credentials must be supplied through `DATABASE_URL`; do not commit `.env` files or real credentials.
- CSV imports should be tested with trusted sample data until validation and error reporting are strengthened.
- Automated tests and a verified public deployment have not yet been established.

## Repository

[View Issue Tracker on GitHub](https://github.com/suresh294/Issue-tracker)
