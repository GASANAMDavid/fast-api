FROM python:3.11-slim

# Install PostgreSQL client and development libraries
RUN apt-get update && apt-get install -y postgresql-client libpq-dev
# Set environment variables
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Ensure the database directory is writable
RUN mkdir -p /app/db && chmod -R 777 /app/db

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
