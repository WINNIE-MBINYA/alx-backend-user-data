#!/usr/bin/env python3
"""User model module."""

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
import hashlib

Base = declarative_base()


class User(Base):
    """User model class."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), nullable=False, unique=True)
    hashed_password = Column(String(128), nullable=False)
    session_id = Column(String(128), nullable=True)
    reset_token = Column(String(128), nullable=True)

    def __init__(self, *args, **kwargs):
        """Initialize the user."""
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self.hashed_password = kwargs.get('hashed_password')

    def __repr__(self):
        """Return string representation of the user."""
        return f"<User(id={self.id}, email={self.email})>"

    def set_password(self, password: str) -> None:
        """Set hashed password."""
        self.hashed_password = hashlib.md5(password.encode()).hexdigest()

    def is_valid_password(self, password: str) -> bool:
        """Check if the provided password is valid."""
        return self.hashed_password == hashlib.md5(
            password.encode()
        ).hexdigest()

    def set_session_id(self, session_id: str) -> None:
        """Set session ID."""
        self.session_id = session_id

    def set_reset_token(self, reset_token: str) -> None:
        """Set reset token."""
        self.reset_token = reset_token

    @staticmethod
    def search(query: dict):
        """Search for users based on the query."""
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import create_engine

        engine = create_engine('sqlite:///my_db.sqlite3')
        Session = sessionmaker(bind=engine)
        session = Session()

        if not query or not isinstance(query, dict):
            return []

        filters = [getattr(User, key) == value for key, value in query.items()]
        return session.query(User).filter(*filters).all()
