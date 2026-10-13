from pydantic import BaseModel
from typing import List, Optional

class IssueCreate(BaseModel):
    title: str
    assignee_id: Optional[int] = None

class IssueUpdate(BaseModel):
    title: str
    version: int

class CommentCreate(BaseModel):
    author: str
    body: str

class LabelReplace(BaseModel):
    labels: List[str]
