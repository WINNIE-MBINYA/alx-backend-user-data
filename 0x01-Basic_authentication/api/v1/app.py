#!/usr/bin/env python3
"""
Route module for the API
This module sets up a Flask application with CORS support and defines
error handlers for various HTTP status codes.

Dependencies:
- Flask: A web framework for Python.
- Flask-CORS: A Flask extension for handling
        Cross-Origin Resource Sharing (CORS).

Usage:
- Run the application by executing this script. The server will listen
  on the host and port specified in the environment variables
  API_HOST and API_PORT, or default to 0.0.0.0 and 5000, respectively.
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.auth.auth import Auth

# Create a Flask application instance
app = Flask(__name__)

# Register the app_views blueprint with the application
app.register_blueprint(app_views)

# Enable CORS for all routes under the /api/v1/ endpoint
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth based on AUTH_TYPE
auth = None
auth_type = getenv("AUTH_TYPE", None)

if auth_type == "auth":
    auth = Auth()


@app.before_request
def before_request_handler():
    """
    Before request handler to filter requests based on authentication.
    """
    if auth is None:
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]

    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """Error handler for 404 Not Found.

    Args:
        error: The error that occurred.

    Returns:
        A JSON response with an error message and a 404 status code.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Error handler for 401 Unauthorized.

    Args:
        error: The error that occurred.

    Returns:
        A JSON response with an error message and a 401 status code.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Error handler for 403 Forbidden.

    Args:
        error: The error that occurred.

    Returns:
        A JSON response with an error message and a 403 status code.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    # Get the host and port from environment variables or use defaults
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    # Run the Flask application
    app.run(host=host, port=port)
