# fastapi/app/models/authuser.py
import logging
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func
from datetime import datetime

from app.db import Base
from .contact import Contact

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


class PrivateContact(Contact, SerializerMixin):
    __tablename__ = "private_contacts"
    __table_args__ = {"sqlite_autoincrement": True}
    __mapper_args__ = {"concrete": True}
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "auth_users.id", ondelete="CASCADE"), nullable=False)
    deletedAt = Column(DateTime, default=None)  # Match database column name
    createdAt = Column(DateTime, default=func.now(), nullable=False)
    updatedAt = Column(DateTime, default=func.now(), nullable=False)
    owner = relationship("AuthUser", back_populates="private_contacts")
    serialize_rules = ("-owner",)

    def __init__(self, firstname, lastname, phone, owner_id):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.owner_id = owner_id
        self.createdAt = func.now()  # Match column name
        self.updatedAt = func.now()  # Match column name

    def delete(self):
        """Soft delete by setting deletedAt."""
        self.deletedAt = datetime.utcnow()  # Match column name
        logger.debug(f"Soft deleted contact: {self.id}")


AuthUser.private_contacts = relationship(
    "PrivateContact",
    back_populates="owner",
    cascade="all, delete-orphan"
)
