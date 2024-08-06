# Basic Authentication API

## Description
This project implements a basic authentication system for a RESTful API using Python and Flask. It includes error handling, user authentication, and basic security measures.

## Installation
1. Clone the repository
2. Install dependencies: `pip3 install -r requirements.txt`
3. Start the server: `API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app`

## Usage
Use the API endpoints to interact with the user data. Authentication is required for protected routes.

## Endpoints
- `/api/v1/status`: Check API status
- `/api/v1/unauthorized`: Simulate unauthorized access
- `/api/v1/forbidden`: Simulate forbidden access

## Authentication
The API uses Basic Authentication. Include an `Authorization` header with your requests to access protected routes.

## Error Handling
The API returns appropriate error messages for `401 Unauthorized` and `403 Forbidden` status codes.
