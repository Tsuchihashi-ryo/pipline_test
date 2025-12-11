# Use an official lightweight Python image.
FROM python:3.9-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements file into the container.
COPY requirements.txt .

# Install the required Python dependencies.
# We use --no-cache-dir to reduce the image size.
RUN pip install --no-cache-dir -r requirements.txt

# The container doesn't need to run a command itself,
# as it will be used as the execution environment for pipeline components.
