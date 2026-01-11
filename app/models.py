from sqlalchemy import (
    Column, Integer, String, Text,
    ForeignKey, DateTime, UniqueConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Issue(Base):
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    status = Column(String, default="open")
    assignee_id = Column(Integer, ForeignKey("users.id"))
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)

    comments = relationship("Comment", back_populates="issue")
    labels = relationship("IssueLabel", back_populates="issue")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    issue_id = Column(Integer, ForeignKey("issues.id"))
    author = Column(String, nullable=False)
    body = Column(Text, nullable=False)

    issue = relationship("Issue", back_populates="comments")

class Label(Base):
    __tablename__ = "labels"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class IssueLabel(Base):
    __tablename__ = "issue_labels"
    issue_id = Column(Integer, ForeignKey("issues.id"), primary_key=True)
    label_id = Column(Integer, ForeignKey("labels.id"), primary_key=True)

    issue = relationship("Issue", back_populates="labels")
