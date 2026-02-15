from sqlalchemy import Column, Integer, String
from app.db import Base  # Import Base from your db setup
from sqlalchemy_serializer import SerializerMixin  # Optional: keep if installed

# If sqlalchemy_serializer isn’t installed, define a dummy mixin
try:
    from sqlalchemy_serializer import SerializerMixin
except ImportError:
    class SerializerMixin:
        pass


class Contact(Base, SerializerMixin):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    phone = Column(String(20))

    def __init__(self, firstname, lastname, phone):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone

    def update(self, firstname, lastname, phone):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
