# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the ports for the application and gRPC server
EXPOSE 5000
EXPOSE 50051

# Default command (can be overridden in docker-compose.yml)
CMD ["sh", "-c", "python main.py"]