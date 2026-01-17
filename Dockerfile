# Use official Python image as base
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Run migrations and collect static files
# We use a shell form to allow chaining commands
RUN python manage.py makemigrations --noinput \
    && python manage.py migrate --noinput \
    && python manage.py collectstatic --noinput
RUN python manage.py collectstatic --noinput


EXPOSE 8000

# Start the server
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

