# Base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHON_ENV=PRODUCTION
ENV HOME=/app

# Create a non-root user and group
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Set working directory and create /app directory with proper permissions
RUN mkdir /app && chown appuser:appgroup /app

# Set working directory
WORKDIR /app

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy Pipfile and Pipfile.lock first to leverage Docker cache
COPY Pipfile Pipfile.lock /app/

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile

# Copy application files
COPY application /app/application
COPY bootstrap.py /app/
COPY migration.py /app/

# Ensure appuser has write permissions to the /app directory
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Run database migrations and start the application
CMD ["pipenv", "run", "python", "bootstrap.py"]