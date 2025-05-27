#!/bin/bash
# Wait for Docker to be ready
while ! docker info &> /dev/null; do
  echo "Waiting for Docker..."
  sleep 3
done

# Run container
docker compose -f /Users/service/github/searchdv/docker-compose.yml up -d

