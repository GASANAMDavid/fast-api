This project is a simple CRUD API with authentication using FastAPI, following best practices.

## Setup

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd fast-api
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file and add your secret key:
    ```env
    SECRET_KEY=your_secret_key
    ```

5. Run the application:
    ```sh
    uvicorn app.main:app --reload
    ```

## Running Tests

To run the tests, use the following command:
```sh
pytest
```

## Endpoints

- `POST /token`: Obtain a token by providing username and password.
- `POST /users/`: Create a new user.
- `GET /users/me/`: Get the current authenticated user's information.
