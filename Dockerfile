# Use the official Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run on container start
CMD ["python", "main.py"]
