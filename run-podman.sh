#!/bin/bash

if ! command -v podman-compose &> /dev/null; then
    echo "podman-compose is not installed. Installing..."
    pip install podman-compose
fi

podman-compose up --build -d

podman-compose ps 