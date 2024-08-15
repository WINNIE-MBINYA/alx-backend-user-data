#!/usr/bin/env python3
"""API application module."""

from flask import Flask, jsonify, request, abort
from auth import Auth, BasicAuth
from db import DB
from user import User

app = Flask(__name__)
auth = BasicAuth()

@app.route('/', methods=['GET'])
def home():
    """Home route."""
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'])
def register_user():
    """Register a new user."""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        user = auth.create_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route('/sessions', methods=['POST'])
def login():
    """Login user and create a session."""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    user = auth.valid_login(email, password)
    if not user:
        abort(401)

    session_id = auth.create_session(user.id)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response

@app.route('/sessions', methods=['DELETE'])
def logout():
    """Logout user and destroy session."""
    session_id = request.cookies.get('session_id')

    if not session_id or not auth.destroy_session(request):
        abort(403)

    return jsonify({"message": "logout successful"}), 200

@app.route('/profile', methods=['GET'])
def profile():
    """Retrieve user profile."""
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200

@app.route('/reset_password', methods=['POST'])
def reset_password():
    """Reset user's password."""
    email = request.form.get('email')

    if not email:
        abort(403)

    try:
        token = auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)

@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Update the password using the reset token."""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(403)

    try:
        auth.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
