# from enum import unique
from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class JobPost(Base):
    __tablename__ = "job-posts"
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    company_name = Column(String(256), nullable=True)
    job_description = Column(String(256), nullable=True)
    skills = Column(String(256), nullable=True)
    job_type = Column(String(256), nullable=True)
    locations = Column(String(256), nullable=True)
    comments = Column(String(256), nullable=True)


class User(Base):
    __tablename__ = "users"
    id = Column(String(256))
    email = Column(String(256), primary_key=True)
    username = Column(String(256), unique=True)
    password = Column(String(256))
    subscribed = Column(Boolean())
