# Use the official image as a parent image
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install PostgreSQL client
RUN apt-get update && apt-get install -y libpq-dev

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install pytest and pytest-cov
RUN pip install pytest pytest-cov

# Copy the project files into the container
COPY . .
