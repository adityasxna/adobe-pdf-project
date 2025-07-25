# Dockerfile

# Use a specific, lightweight Python base image.
# Using linux/amd64 ensures compatibility with most cloud judging environments.
FROM --platform=linux/amd64 python:3.9-slim-buster

# Set the working directory inside the container to /app
# All subsequent commands will run from this directory.
WORKDIR /app

# Copy the requirements file first. Docker caches this layer.
# If requirements.txt doesn't change, this step won't re-run on future builds, speeding things up.
COPY requirements.txt .

# Install the Python dependencies specified in requirements.txt.
# --no-cache-dir saves space in the final image.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire 'app' directory (containing all your Python code) into the container's /app directory.
COPY ./app/ .

# This is the command that will be executed when the container starts.
# It runs your main script.
CMD ["python", "main.py"]