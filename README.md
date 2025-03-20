
<div align="center">

![Python](https://img.shields.io/badge/Python-3.11.11%2B-blue)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Docs](https://github.com/ividal/robustness-scans/actions/workflows/docs.yaml/badge.svg)](https://github.com/ividal/robustness-scans/actions/workflows/docs.yaml/)
[![Tests](https://github.com/ividal/robustness-scans/actions/workflows/tests.yaml/badge.svg)](https://github.com/ividal/robustness-scans/actions/workflows/tests.yaml/)
[![Ruff](https://github.com/ividal/robustness-scans/actions/workflows/lint.yaml/badge.svg?label=Ruff)](https://github.com/ividal/robustness-scans/actions/workflows/lint.yaml/)

**Repository template courtesy of the [Blueprints Hub](https://developer-hub.mozilla.ai/).**

</div>


# How to... Scan an LLM app for vulnerabilities

This repo shows you to in testing your Q&A application. Do you want to know if it tends to hallucinate? Or whether it may be easily convinced of the opposite of what it reads? Jailbreaks? You can scan for it.

All you need is:
* For your toy Q&A app:
   * [Langchain](https://github.com/langchain-ai/langchain) and particularly [Langchain-Community](https://python.langchain.com/api_reference/community/index.html) to build a sample Q&A chatbot on PDFs. This will play the part of the system you want to probe.
   * [PyPDF](https://github.com/py-pdf/pypdf/) to parse the PDFs.
   * [Llamafile](https://github.com/Mozilla-Ocho/llamafile) or an API key for Mistral for the LLM at the core of the sample app.
* For the demo UI:
   * [Streamlit](https://streamlit.io/)
* For the actual scanning and probing:
   * [Giskard](https://github.com/Giskard-AI/giskard)


## Quick-start

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mozilla-ai/blueprint-template.git
   cd blueprint-template
   ```

2. Install `uv`:

   **On Ubuntu 24.04**:
   ```bash
   sudo apt update
   sudo apt install -y make build-essential libssl-dev zlib1g-dev \
   libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
   libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev \
   liblzma-dev python-openssl git
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   **On macOS**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Install Python with `uv`:
   ```bash
   uv python install 3.11.11
   ```

4. Create a virtual environment and handle dependencies with `uv`:
   ```bash
   uv venv
   ```

5. Install the package:
   ```bash
   uv sync
   ```

### Running the application

To start the demo application:
```bash
cd demo
uv run streamlit run app.py
```

This will launch a Streamlit web interface at http://localhost:8501 displaying a simple "Hello, world!" message.

## Using Docker

### Building and running with Docker

1. Build the Docker image:
   ```bash
   docker build -t blueprint .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 blueprint
   ```

3. Access the application at http://localhost:8501

## Documentation

### Building and viewing the docs

1. Install the documentation dependencies:
   ```bash
   # Using uv
   uv sync --all-groups
   ```

2. Build and serve the documentation:
   ```bash
   uv run mkdocs serve
   ```

3. View the documentation at http://localhost:8000

### Building the docs for production

```bash
uv run mkdocs build
```

The built documentation will be available in the `site` directory.

## Testing

### Running tests

1. Install test dependencies:
   ```bash
   # Using uv
   uv sync --all-groups
   ```

2. Run the tests:
   ```bash
   uv run pytest -v tests/
   ```


## How it Works


## Pre-requisites

- **System requirements**:
  - OS: Windows, macOS, or Linux
  - Python 3.11.11 or higher
  - Minimum RAM:
  - Disk space:

- **Dependencies**:
  - Dependencies listed in `pyproject.toml`


## Troubleshooting


## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! To get started, you can check out the [CONTRIBUTING.md](CONTRIBUTING.md) file.
