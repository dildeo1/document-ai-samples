FROM node:21-slim

# Specify a non-root user
USER node

# Set environment variables
ENV APP_HOME /app
WORKDIR $APP_HOME

# Copy all files to the WORKDIR
COPY --chown=node:node . ./

# Change to the Frontend directory
WORKDIR /app/Frontend

# Install dependencies and build the project
RUN npm install && npm run build

# Add a HEALTHCHECK instruction
HEALTHCHECK CMD curl --fail http://localhost:8080/ || exit 1

# Expose the desired port
EXPOSE 8080

# Start the application
CMD [ "node", "server.js" ]
