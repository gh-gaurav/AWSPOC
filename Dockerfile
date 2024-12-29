FROM python:3.12.7-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory content into the container at /app
COPY . /app/

# Update the package list and install AWS CLI
RUN apt-get update -y && apt-get install -y awscli

# Install required Python packages
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set the default command to run your Flask app (assuming app.py is the entry point)
CMD ["python3", "app.py"]
