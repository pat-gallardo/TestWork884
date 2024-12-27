# Financial Transaction Analysis Microservice

This is a microservice that uses REST API endpoints for managing financial transactions.

## Features
- Simple transaction management
- Statistical Analysis
- API Authentication

## Running Locally

1. Create a .env file with:
```
DATABASE_URL = postgresql://user:password@localhost:5432/transactions_db
REDIS_URL = redis://localhost:6379/0
API_KEY = your_secret_api_key
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start PostgreSQL and Redis Server

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## Running with Docker Compose

1. Build and start the services:
```bash
docker-compose up --build
```

The API will be available at http://localhost:8000

## API Documentation

Access the Swagger documentation at http://localhost:8000/docs

## API Endpoints

- POST /transactions - Create a new transaction
- DELETE /transactions - Delete all transactions
- GET /statistics - Get transaction statistics

## Authentication

Add the API key to requests using the Authorization header:
```
Authorization: ApiKey your_secret_api_key
```

## Running Tests

```bash
pytest app/tests/tests_api.py
```