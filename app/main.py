from fastapi import FastAPI, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
import pandas as pd

from .database import SessionLocal, engine
from . import models, schemas, crud, reports

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Issue Tracker API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/issues")
def create_issue(data: schemas.IssueCreate, db: Session = Depends(get_db)):
    issue = models.Issue(**data.dict())
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue


@app.get("/issues")
def list_issues(db: Session = Depends(get_db)):
    return db.query(models.Issue).all()


@app.get("/issues/{id}")
def get_issue(id: int, db: Session = Depends(get_db)):
    issue = db.get(models.Issue, id)
    if not issue:
        raise HTTPException(404, "Issue not found")
    return issue


@app.patch("/issues/{id}")
def update_issue(id: int, data: schemas.IssueUpdate, db: Session = Depends(get_db)):
    return crud.update_issue_with_version(db, id, data.title, data.version)


@app.post("/issues/{id}/comments")
def add_comment(id: int, c: schemas.CommentCreate, db: Session = Depends(get_db)):
    if not c.body.strip():
        raise HTTPException(400, "Comment body cannot be empty")
    if not db.get(models.Issue, id):
        raise HTTPException(404, "Issue not found")

    comment = models.Comment(issue_id=id, **c.dict())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@app.put("/issues/{id}/labels")
def replace_labels(id: int, data: schemas.LabelReplace, db: Session = Depends(get_db)):
    if not db.get(models.Issue, id):
        raise HTTPException(404, "Issue not found")

    labels = [name.strip() for name in data.labels]
    if any(not name for name in labels):
        raise HTTPException(400, "Label names cannot be empty")
    labels = list(dict.fromkeys(labels))

    try:
        db.query(models.IssueLabel).filter_by(issue_id=id).delete(synchronize_session=False)

        for name in labels:
            label = db.query(models.Label).filter_by(name=name).first()
            if not label:
                label = models.Label(name=name)
                db.add(label)
                db.flush()

            db.add(models.IssueLabel(issue_id=id, label_id=label.id))

        db.commit()
        return {"labels": labels}
    except Exception:
        db.rollback()
        raise HTTPException(500, "Unable to replace issue labels")


@app.post("/issues/bulk-status")
def bulk_status(ids: list[int], status: str, db: Session = Depends(get_db)):
    if not ids:
        raise HTTPException(400, "At least one issue ID is required")
    if not status.strip():
        raise HTTPException(400, "Status cannot be empty")
    crud.bulk_update_status(db, ids, status)
    return {"updated": len(ids)}


@app.post("/issues/import")
def import_csv(file: UploadFile, db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(file.file)
    except Exception:
        raise HTTPException(400, "Unable to read CSV file")

    required_columns = {"title", "assignee_id"}
    if not required_columns.issubset(df.columns):
        raise HTTPException(400, "CSV must contain title and assignee_id columns")

    success, failed = 0, 0
    for _, row in df.iterrows():
        try:
            title = str(row["title"]).strip()
            if not title:
                failed += 1
                continue

            assignee_value = row["assignee_id"]
            assignee_id = None if pd.isna(assignee_value) else int(assignee_value)
            db.add(models.Issue(title=title, assignee_id=assignee_id))
            db.flush()
            success += 1
        except (TypeError, ValueError):
            db.rollback()
            failed += 1

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(400, "CSV import could not be committed")

    return {"success": success, "failed": failed}


@app.get("/reports/top-assignees")
def report_assignees(db: Session = Depends(get_db)):
    return reports.top_assignees(db)


@app.get("/reports/latency")
def report_latency(db: Session = Depends(get_db)):
    return reports.average_resolution_time(db)
