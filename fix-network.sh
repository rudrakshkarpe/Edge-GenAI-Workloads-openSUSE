#!/bin/bash

# Remove existing CNI configs
sudo rm -rf /etc/cni/net.d/*
sudo rm -rf ~/.config/cni/net.d/*

# Create proper CNI config
sudo mkdir -p /etc/cni/net.d/
sudo tee /etc/cni/net.d/87-podman-bridge.conflist << EOF
{
  "cniVersion": "0.4.0",
  "name": "podman",
  "plugins": [
    {
      "type": "bridge",
      "bridge": "cni-podman0",
      "isGateway": true,
      "ipMasq": true,
      "ipam": {
        "type": "host-local",
        "ranges": [
          [
            {
              "subnet": "10.88.0.0/16"
            }
          ]
        ]
      }
    },
    {
      "type": "portmap",
      "capabilities": {
        "portMappings": true
      }
    }
  ]
}
EOF 