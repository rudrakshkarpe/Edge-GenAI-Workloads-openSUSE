#!/bin/bash

# Create proper CNI config
sudo mkdir -p /etc/cni/net.d/
sudo tee /etc/cni/net.d/99-podman.conflist << EOF
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

# Fix registries configuration
sudo mkdir -p /etc/containers
sudo tee /etc/containers/registries.conf << EOF
unqualified-search-registries = ["docker.io", "quay.io"]

[[registry]]
prefix = "docker.io"
location = "docker.io"

[[registry]]
prefix = "quay.io"
location = "quay.io"

[[registry]]
prefix = "registry.opensuse.org"
location = "registry.opensuse.org"
EOF

# Create containers policy
sudo tee /etc/containers/policy.json << EOF
{
    "default": [
        {
            "type": "insecureAcceptAnything"
        }
    ]
}
EOF 