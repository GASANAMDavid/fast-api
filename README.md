# FastAPI Project

This project is built with FastAPI and includes the following routes:

## Authentication Routes

- **POST /auth/token**: Obtain an access token by providing username and password.

## User Routes

- **POST /users/**: Create a new user.
- **GET /users/me/**: Get the current authenticated user's information.

## Article Routes

- **POST /articles/**: Create a new article.
- **GET /articles/**: Get a list of articles.
- **GET /articles/{article_id}**: Get a specific article by ID.
- **PUT /articles/{article_id}**: Update a specific article by ID.
- **DELETE /articles/{article_id}**: Delete a specific article by ID.

## Setup

### Environment Variables

Create environment variable files in the project root by copying the `.env.sample` file:

- **.env** (for development):
  ```sh
  cp .env.sample .env
  ```

- **.env.test** (for testing):
  ```sh
  cp .env.sample .env.test
  ```

Then, adjust the values in the `.env` and `.env.test` files as needed.

### Docker Setup

1. **Build and run the Docker containers**:
    ```sh
    docker-compose up --build
    ```

2. **Run the Alembic migrations**:
    ```sh
    docker-compose run web alembic upgrade head
    ```

3. **Run the tests**:
    ```sh
    docker-compose run web pytest --disable-warnings
    ```

### Non-Docker Setup

1. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

2. **Set up the database**:
    - Ensure you have PostgreSQL installed and running.

3. **Run the Alembic migrations**:
    ```sh
    alembic upgrade head
    ```

4. **Run the application**:
    ```sh
    uvicorn app.main:app --reload
    ```

5. **Run the tests**:
    ```sh
    ENV_TEST=1 pytest --disable-warnings
    ```

## Access the API documentation

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)