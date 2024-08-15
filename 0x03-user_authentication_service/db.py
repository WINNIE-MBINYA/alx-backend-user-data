#!/usr/bin/env python3
"""DB module for managing the database."""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from typing import TypeVar, List


Base = declarative_base()


class User(Base):
    """User model to represent a user in the database."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(128), nullable=False)
    hashed_password = Column(String(128), nullable=False)
    session_id = Column(String(128))
    reset_token = Column(String(128))


class DB:
    """DB class to interact with the database."""

    def __init__(self) -> None:
        """Initialize the database connection."""
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.create_all(self._engine)
        self._session = sessionmaker(bind=self._engine)()

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database."""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database by various attributes."""
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise ValueError("No user found with given attributes")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes."""
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")
        self._session.commit()
