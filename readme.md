# Issue Tracker API

A backend service built using FastAPI and PostgreSQL to manage issues, comments, and labels.

## Features
- Issue CRUD with optimistic locking
- Comments with validation
- Unique labels per issue
- Transactional bulk updates
- CSV import with summary
- Aggregated reports

## Run
pip install -r requirements.txt  
uvicorn app.main:app --reload
