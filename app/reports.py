from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import Issue

def top_assignees(db: Session):
    return db.query(
        Issue.assignee_id,
        func.count(Issue.id)
    ).group_by(Issue.assignee_id).all()

def average_resolution_time(db: Session):
    return db.query(
        func.avg(Issue.resolved_at - Issue.created_at)
    ).filter(Issue.resolved_at != None).scalar()
