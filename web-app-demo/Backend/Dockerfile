# Use the official lightweight Python image.
# https://hub.docker.com/_/python
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

# Update pip as the root user
RUN pip install --upgrade pip

# Install production dependencies as the root user
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8080

# Switch to the non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD curl --fail http://localhost:8080/ || exit 1

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.

CMD ["gunicorn", "--bind", ":$PORT", "--workers", "1", "--threads", "8", "--timeout", "0", "main:app"]
