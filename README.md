# Social-Media-Backend
# Social Media App

A robust backend system for a social media application built using Django and Django REST Framework. This backend supports user authentication, allows users to create and interact with posts, manage connections, and implements features that enhance user engagement and connectivity.

## Features

- User authentication using Knox token-based authentication.
- User registration and login.
- User profile management.
- Post creation, retrieval, like, and unlike functionalities.
- Connection management, including sending and accepting connection requests.
- Recommendation feature to suggest users to connect with based on mutual connections or common interests.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/pathangufran/Social-Media-Backend.git
    ```

2. Navigate to the project directory:

    ```bash
    cd social_media_app
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

5. Run the development server:

    ```bash
    python manage.py runserver
    ```

## Usage

1. Register a new user:

    ```bash
    curl -X POST http://127.0.0.1:8000/api/register/ -H 'Content-Type: application/json' -d '{"username": "new_user", "email": "new_user@example.com", "password": "your_password"}'
    ```

2. Login to obtain a token:

    ```bash
    curl -X POST http://127.0.0.1:8000/api/login/ -H 'Content-Type: application/json' -d '{"username": "new_user", "password": "your_password"}'
    ```

3. Access user profile:

    ```bash
    curl -X GET http://127.0.0.1:8000/api/profile/ -H 'Authorization: Token <your_token>'
    ```

4. Create a new post:

    ```bash
    curl -X POST http://127.0.0.1:8000/api/posts/ -H 'Authorization: Token <your_token>' -H 'Content-Type: application/json' -d '{"title": "New Post", "content": "This is the content of the post."}'
    ```

5. Retrieve list of posts:

    ```bash
    curl -X GET http://127.0.0.1:8000/api/posts/ -H 'Authorization: Token <your_token>'
    ```

6. Like a post:

    ```bash
    curl -X POST http://127.0.0.1:8000/api/posts/<post_id>/like/ -H 'Authorization: Token <your_token>'
    ```

7. Unlike a post:

    ```bash
    curl -X DELETE http://127.0.0.1:8000/api/posts/<post_id>/unlike/ -H 'Authorization: Token <your_token>'
    ```

8. Send a connection request:

    ```bash
    curl -X POST http://127.0.0.1:8000/api/connections/send/<to_user_id>/ -H 'Authorization: Token <your_token>'
    ```

9. Accept a connection request:

    ```bash
    curl -X PUT http://127.0.0.1:8000/api/connections/accept/<connection_id>/ -H 'Authorization: Token <your_token>'
    ```

10. Get recommended connections:

    ```bash
    curl -X GET http://127.0.0.1:8000/api/connections/recommend/ -H 'Authorization: Token <your_token>'
    ```
