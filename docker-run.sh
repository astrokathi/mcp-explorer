#!/bin/bash
set -e

ENV_FILE=".env"

echo "Starting Docker Compose stack using $ENV_FILE..."
docker compose --env-file $ENV_FILE up -d --build

echo ""
echo "All services started!"
echo "Access Langfuse UI at: http://localhost:3000"
echo "Access Chainlit App at: http://localhost:8000"
