# Use the official lightweight Python image
FROM python:3.11-slim

# Create a non-root user to run the application
RUN adduser --system --group --disabled-password appuser

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Set environment variable for the application home directory
ENV APP_HOME /app

# Set the working directory
WORKDIR $APP_HOME

# Copy local code to the container image
COPY . ./

# Update pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Gunicorn is installed
RUN pip install gunicorn

# Expose the port the app runs on
EXPOSE 8080

# Switch to the non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD curl --fail http://localhost:$PORT/ || exit 1

# Run the web service on container startup
CMD exec gunicorn --bind "0.0.0.0:${PORT}" --workers 1 --threads 8 --timeout 0 main:app
