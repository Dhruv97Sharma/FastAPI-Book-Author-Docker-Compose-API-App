# Docker Containerized FastAPI app

This repository is a book-author docker-compose containerised app managing FastAPI, Postgres services.

# Tutorial

pip install fastapi fastapi-sqlalchemy pydantic alembic psycopg2 uvicorn python-dotenv

# To run and apply migrations

docker-compose run app alembic revision --autogenerate -m "New Migration"
docker-compose run app alembic upgrade head

### Remember to make a note that the version of docker-compose used here is 2.4

docker-compose build
docker-compose up