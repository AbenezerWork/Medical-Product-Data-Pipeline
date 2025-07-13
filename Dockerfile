# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
COPY . .

# Make port 8000 available to the world outside this container (for FastAPI)
EXPOSE 8000

# Define the command to run your application
# This might change depending on which part of the project you're running
# For now, a simple command is fine.
CMD ["tail", "-f", "/dev/null"]
