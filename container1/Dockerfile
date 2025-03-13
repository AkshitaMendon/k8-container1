# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files
COPY app.py requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 6000

# Run application
CMD ["python", "app.py"]