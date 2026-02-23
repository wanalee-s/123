# fastapi/app/models/authuser.py
import logging
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func
from datetime import datetime

from app.db import Base

logger = logging.getLogger(__name__)

class AuthUser(Base, SerializerMixin):
    __tablename__ = "auth_users"
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(1000))
    avatar_url = Column(String(100))
    password_hash = Column(String(255), nullable=True)  # Allow null for OAuth users

    def __init__(self, email, name, avatar_url=None, password_hash=None):
        self.email = email
        self.name = name
        self.avatar_url = avatar_url
        self.password_hash = password_hash

    def update(self, email, name, avatar_url=None, password_hash=None):
        self.email = email
        self.name = name
        self.avatar_url = avatar_url
        self.password_hash = password_hash

