from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from . import models

def update_issue_with_version(db: Session, issue_id: int, title: str, version: int):
    issue = db.query(models.Issue).get(issue_id)
    if not issue:
        raise HTTPException(404, "Issue not found")

    if issue.version != version:
        raise HTTPException(409, "Version conflict")

    issue.title = title
    issue.version += 1
    db.commit()
    return issue

def bulk_update_status(db: Session, issue_ids, status):
    try:
        for issue_id in issue_ids:
            issue = db.query(models.Issue).get(issue_id)
            if not issue:
                raise Exception("Invalid issue ID")

            issue.status = status
            if status == "resolved":
                issue.resolved_at = datetime.utcnow()

        db.commit()
    except:
        db.rollback()
        raise HTTPException(400, "Bulk update failed")
