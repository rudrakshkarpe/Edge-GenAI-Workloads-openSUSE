# Edge-GenAI-Workloads-openSUSE 🚀

A retrieval augmented generation (RAG) platform with open-source Large Language Models (LLMs) without exposing your data to online LLM providers.

<details>
<summary>Table of Contents</summary>

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Development](#development)
- [Containerization](#containerization)
- [Contributing](#contributing)

</details>

## Overview

This project enables local LLM deployment with RAG capabilities, specifically designed for edge computing environments. It uses Ollama for LLM serving and supports various document types for context-aware conversations.

## Features

- 🤖 Local LLM deployment using Ollama
- 📚 RAG (Retrieval Augmented Generation) support
- 🔒 Privacy-focused (all data stays local)
- 🌐 Multiple input sources:
  - GitHub repositories
  - Web pages
  - Local documents
- 🖥️ Containerized deployment with Podman
- 🎯 Optimized for edge devices

## Prerequisites

<details>
<summary>System Requirements</summary>

- Python 3.10+
- CUDA-capable GPU (optional, but recommended)
- 8GB RAM minimum (16GB recommended)
- Ubuntu/openSUSE system

</details>

<details>
<summary>Required Dependencies</summary>

1. **Ollama Installation**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. **Podman Setup (Ubuntu)**
```bash
# Run the setup script
chmod +x setup-ubuntu-host.sh
./setup-ubuntu-host.sh
```

3. **Python Dependencies**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Clone the Repository**
```bash
git clone https://github.com/rudrakshkarpe/Edge-GenAI-Workloads-openSUSE.git
cd Edge-GenAI-Workloads-openSUSE
```
</details>

<details>
<summary>2. Configure Environment</summary>

```bash
# Setup networking
chmod +x fix-network.sh
./fix-network.sh

# Configure Podman
chmod +x fix-podman-config.sh
./fix-podman-config.sh
```
</details>

<details>
<summary>3. Start the Application</summary>

```bash
# Start containers
chmod +x start-containers.sh
./start-containers.sh

# Access the application
open http://localhost:<your-port>
```
</details>

## Project Structure

<details>
<summary>Directory Layout</summary>

```
Edge-GenAI-Workloads-openSUSE/
├── components/         # UI components
├── modules/           # Core modules
├── utils/            # Utility functions
├── docs/             # Documentation
└── scripts/          # Shell scripts
```
</details>

## Usage

<details>
<summary>Setting up Embeddings</summary>

The project uses HuggingFace embeddings for document processing. The embedding setup is handled in:

```bash
utils/llama_index.py
```

Key features:
- Automatic GPU detection
- Configurable embedding models
- Caching for better performance
</details>

<details>
<summary>Using Ollama Models</summary>

1. Pull a model:
```bash
ollama pull mistral
```

2. The Ollama integration is managed in:
```bash
utils/ollama.py
```

3. Models are automatically detected and listed in the UI
</details>

<details>
<summary>Document Processing</summary>

The system supports multiple document sources:

- "pdf", "txt", "doc", "docx"
</details>

## Development

<details>
<summary>Local Development Setup</summary>

1. Create a virtual environment
2. Install dependencies
3. Run Streamlit locally:
```bash
streamlit run main.py
```
</details>

## Containerization

<details>
<summary>Container Setup</summary>

The project uses Podman for containerization:

<!-- 1. Dockerfile.podman:
```dockerfile:Dockerfile.podman
startLine: 1
endLine: 42
``` -->

<!-- 2. Container composition:
```yaml:podman-compose.yml
startLine: 1
endLine: 25
``` -->

3. Start containers:
```bash
./start-containers.sh
```
</details>

## Contributing

<details>
<summary>How to Contribute</summary>

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please follow the project's coding standards and include tests for new features.
</details>

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

[Google Summer of Code 2024 @ openSUSE Project](https://summerofcode.withgoogle.com/programs/2024/projects/qmkkFMtn)