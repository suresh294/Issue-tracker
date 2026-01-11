Issue Tracker API

A backend service built using Python (FastAPI) and PostgreSQL to manage issues, comments, and labels.
This project demonstrates real-world backend concepts such as optimistic concurrency control, transactions, bulk operations, and CSV imports.

✨ Features
Create, update, list, and view issues
Optimistic locking using versioning
Add comments with validation
Assign and replace labels atomically
Transactional bulk status updates
CSV import for bulk issue creation
Aggregated reports:
   Top assignees
   Average issue resolution time

🛠 Tech Stack
Backend: Python, FastAPI
Database: PostgreSQL
ORM: SQLAlchemy
API Docs: Swagger (OpenAPI)

## Run
pip install -r requirements.txt  
uvicorn app.main:app --reload
