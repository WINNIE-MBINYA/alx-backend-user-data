#!/usr/bin/env python3
"""Module for Basic Authentication

This module defines the `BasicAuth` class, which implements Basic
Authentication for managing user authentication in an API. It
provides methods to decode Base64 authorization headers, allowing
for the retrieval of user credentials from the authorization
header.

Classes:
    BasicAuth: A class that provides methods for decoding
               Base64 authorization headers.

Methods:
    decode_base64_authorization_header(self,
    base64_authorization_header: str) -> str:
        Decodes the Base64 authorization header to retrieve
        user credentials in UTF-8 format.
    extract_user_credentials(self, decoded_base64_authorization_header: str)
        -> Tuple[Optional[str], Optional[str]]:
        Extracts user email and password from the Base64 decoded value.
    user_object_from_credentials(self, user_email: str, user_pwd: str)
        -> Optional[User]:
        Retrieves the User instance based on the provided email and password.
    current_user(self, request=None) -> Optional[User]:
        Retrieves the User instance for the given request.
"""

from typing import Optional, Tuple
from api.v1.auth.auth import Auth
import base64  # Standard Library for Base64 encoding and decoding
from models.user import User  # Import User model
from typing import List, Optional


class BasicAuth(Auth):
    """ Basic Authentication class """

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> Optional[str]:
        """
        Decodes the Base64 authorization header.

        Args:
            base64_authorization_header (str): The Base64 string.

        Returns:
            str: The decoded string in UTF-8 format, or None
                 if decoding fails or the input is invalid.
        """
        if base64_authorization_header is None or \
                not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None  # Return None if decoding fails

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> \
            Tuple[Optional[str], Optional[str]]:
        """Extracts user email and password from the Base64 decoded value.

        Args:
            decoded_base64_authorization_header (str):
            The decoded Base64 string.

        Returns:
            tuple: A tuple containing the user email and password, or
                   (None, None) if the input is invalid.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split only on the first occurrence of ':'
        user_credentials = decoded_base64_authorization_header.split(":", 1)
        return user_credentials[0], user_credentials[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> Optional[User]:
        """Retrieves a User instance based on email and password.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance if found and password is valid,
            or None if not.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users:
                return None
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> Optional[User]:
        """Retrieves the current User instance based on the request.

        Args:
            request: The Flask request object. Defaults to None.

        Returns:
            User: The User instance associated with the request,
            or None if not found.
        """
        auth_header = self.authorization_header(request)
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        decoded_b64 = self.decode_base64_authorization_header(b64_auth_header)
        user_email, user_pwd = self.extract_user_credentials(decoded_b64)
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user

    def require_auth(
        self, path: Optional[str], excluded_paths: Optional[List[str]]
    ) -> bool:
        """Determine if a given path requires authentication.

        Args:
            path: The path to check (e.g., "/api/v1/status").
            excluded_paths: A list of paths that are excluded from
                            authentication. Wildcards ('*') are
                            supported at the end of paths.

        Returns:
            True if the path requires authentication, False otherwise.
        """
        if path is None or not excluded_paths:
            return True

        path = path.rstrip('/')

        for ep in excluded_paths:
            if ep.endswith('*'):
                if path.startswith(ep[:-1]):
                    return False
            elif path == ep.rstrip('/'):
                return False

        return True
