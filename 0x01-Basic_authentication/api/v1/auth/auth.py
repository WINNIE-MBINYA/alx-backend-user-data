#!/usr/bin/env python3
"""Module for API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that are
                                        excluded from authentication.

        Returns:
            bool: False for now, will be implemented later.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: None for now, will be implemented later.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user based on the request.

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'): None for now, will be implemented later.
        """
        return None
