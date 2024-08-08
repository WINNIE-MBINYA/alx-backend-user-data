#!/usr/bin/env python3
"""Module for API authentication

This module defines the `Auth` class, which serves as a template for
managing API authentication in a Flask application. It provides
methods to determine if a given path requires authentication,
retrieve the authorization header from a request, and identify
the current user based on the request.

Classes:
    Auth: A class that defines methods for managing API authentication.

Methods:
    require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        Determines if a given path requires authentication.

    authorization_header(self, request=None) -> str:
        Returns the authorization header from the request.

    current_user(self, request=None) -> TypeVar('User'):
        Returns the current user based on the request.
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    The `Auth` class provides methods to manage API authentication.

    This class is intended to be a base class for implementing
    different authentication mechanisms. The methods are currently
    placeholders and will be implemented in subclasses or extended
    later.

    Methods:
        require_auth: Determines if a given path requires authentication.
        authorization_header: Returns the authorization header
                              from the request.
        current_user: Returns the current user based on the request.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication.

        Args:
            path (str): The path to check for authentication
                        requirement.
            excluded_paths (List[str]): A list of paths that are
                                        excluded from authentication.

        Returns:
            bool: True if the path requires authentication,
                  False otherwise.

            Returns True if:
                - The path is None.
                - excluded_paths is None or an empty list.

            Returns False if:
                - The path is in excluded_paths or matches
                  an excluded path.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True

        # Ensure the path ends with a slash for comparison
        if not path.endswith('/'):
            path += '/'

        # Check if the path is in the excluded paths
        for excluded_path in excluded_paths:
            if excluded_path.endswith('/'):
                if path == excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from the request.

        Args:
            request: The Flask request object. Defaults to None.

        Returns:
            str: None for now, indicating that no authorization
                 header is returned.
                 This will be implemented later to extract the
                 authorization header from the request.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user based on the request.

        Args:
            request: The Flask request object. Defaults to None.

        Returns:
            TypeVar('User'): None for now, indicating that the
                             current user is not determined.
                             This will be implemented later to
                             return the user based on the
                             authentication details in the request.
        """
        return None
