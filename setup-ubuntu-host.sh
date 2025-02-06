#!/bin/bash

# Install Podman and NVIDIA Container Toolkit on Ubuntu
echo "Installing Podman and NVIDIA tools..."
. /etc/os-release
echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
curl -L "https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/Release.key" | sudo apt-key add -

sudo apt-get update
sudo apt-get install -y podman podman-compose

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit-base
sudo nvidia-ctk runtime configure --runtime=podman

# Create proper registries configuration
sudo mkdir -p /etc/containers
cat << EOF | sudo tee /etc/containers/registries.conf
[registries.search]
registries = ['docker.io', 'registry.opensuse.org']

[registries.insecure]
registries = []

[registries.block]
registries = []
EOF

# Create storage configuration
cat << EOF | sudo tee /etc/containers/storage.conf
[storage]
driver = "overlay"
runroot = "/run/containers/storage"
graphroot = "/var/lib/containers/storage"
EOF

# Pull required images
echo "Pulling required images..."
podman pull docker.io/ollama/ollama:latest

# Create required directories
mkdir -p ~/.local/share/containers/storage/volumes/ollama-data/_data

echo "Setup complete! You can now run podman-compose up --build" 