# Use the official Python image for Windows Server Core
FROM python:3.9slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the ports for the application and gRPC server
EXPOSE 5000
EXPOSE 50051

# Run both the main application and the gRPC server
CMD ["sh", "-c", "python main.py & python app/gRPC_server.py"]
