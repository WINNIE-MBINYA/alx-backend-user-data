#!/usr/bin/env python3
"""Auth module for API authentication."""

from flask import request
from typing import List, TypeVar
import re


class Auth:
    """Auth class for authentication in API."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if the path requires authentication."""
        if not path or not excluded_paths:
            return True

        for p in excluded_paths:
            if p.endswith('*'):
                if path.startswith(p[:-1]):
                    return False
            elif path == p or path == p.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Get the Authorization header from the request."""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user based on the request."""
        return None


class BasicAuth(Auth):
    """BasicAuth class for Basic Authentication."""

    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """Extract the Base64 part from the Authorization header."""
        if not auth_header or not auth_header.startswith('Basic '):
            return None
        return auth_header.split(' ', 1)[1]

    def decode_base64_authorization_header(self, b64_auth_header: str) -> str:
        """Decode the Base64 Authorization header."""
        if not b64_auth_header:
            return None
        try:
            return base64.b64decode(b64_auth_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_header: str) -> (str, str):
        """Extract user credentials from the decoded header."""
        if not decoded_header or ':' not in decoded_header:
            return None, None
        return tuple(decoded_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Get the User object based on email and password."""
        if not user_email or not user_pwd:
            return None

        try:
            user = User.search({"email": user_email})
            if not user:
                return None
            if user.is_valid_password(user_pwd):
                return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current authenticated user."""
        auth_header = self.authorization_header(request)
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(b64_auth_header)
        email, password = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(email, password)
