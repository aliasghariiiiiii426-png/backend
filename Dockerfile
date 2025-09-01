FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Copy project
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt