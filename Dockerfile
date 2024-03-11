# Use Python 3.8.18 image as base
FROM python:3.8.18

# Set the working directory in the container
WORKDIR /app
ENV PIP_TIMEOUT=120

# Copy the current directory contents into the container
ADD . /app
ADD app.py /app/

# Install dependencies

RUN pip install flask flask-cors requests jina
RUN pip install docarray==0.21.0

# Expose port 5000
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
