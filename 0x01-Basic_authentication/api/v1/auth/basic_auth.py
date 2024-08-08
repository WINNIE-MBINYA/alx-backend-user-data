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
"""

from api.v1.auth.auth import Auth
import base64  # Standard Library for Base64 encoding and decoding


class BasicAuth(Auth):
    """ Basic Authentication class """

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 authorization header.

        Args:
            base64_authorization_header (str): The Base64 string.

        Returns:
            str: The decoded string in UTF-8 format, or None
                 if decoding fails or the input is invalid.
        """
        # Check if the input is None or not a string
        if base64_authorization_header is None or \
                not isinstance(base64_authorization_header, str):
            return None
        try:
            # Decode the Base64 authorization header
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')  # Convert bytes to UTF-8 string
        except Exception:
            return None  # Return None if decoding fails
