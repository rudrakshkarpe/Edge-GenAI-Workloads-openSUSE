#!/bin/bash

echo "Cleaning up existing containers..."
podman rm -f ollama-service llm-app 2>/dev/null || true

echo "Running network fix..."
./fix-network.sh

echo "Pulling Ollama image..."
podman pull docker.io/ollama/ollama:latest

echo "Starting Ollama container first..."
podman run -d \
    --name ollama-service \
    -p 11435:11434 \
    -v ollama-data:/root/.ollama \
    docker.io/ollama/ollama:latest

echo "Waiting for Ollama to initialize..."
sleep 10  # Give Ollama time to start up

echo "Starting the full stack..."
podman-compose up --build -d

echo "Checking container status..."
podman ps -a 