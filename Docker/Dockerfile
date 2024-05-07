# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to the outside world (adjust if needed)
EXPOSE 5000

# Define environment variables
ENV FLASK_APP=app.py

# Define environment variables to connect to RDS database (replace with actual values)
ENV RDS_HOST=<your_rds_endpoint>
ENV RDS_USER=<your_rds_username>
ENV RDS_PASSWORD=<your_rds_password>
ENV RDS_DB_NAME=<your_rds_database_name>

# Run app.py when the container launches
CMD ["python", "app.py",\
  "--host=0.0.0.0",\
  "--port=5000",\
  "--db-host=$RDS_HOST",\
  "--db-user=$RDS_USER",\
  "--db-password=$RDS_PASSWORD",\
  "--db-name=$RDS_DB_NAME"\
]
