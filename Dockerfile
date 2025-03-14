# Lightweight Python base image
FROM python:3.9-slim

# Creating and setting up the working directory.
WORKDIR /app

# Copying the requirements file into the container.
COPY requirements.txt .

# Installing Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copying the application code.
COPY app.py .

# Exposing the port on which Flask apps runs.
EXPOSE 8080

# Default command to run the app.
CMD ["python", "app.py"]
