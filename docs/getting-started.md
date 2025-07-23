# Getting Started

Get started with Robustness Scans using one of the options below:

---

## **Prerequisites**

Before you begin, ensure you have:
- **OS**: macOS or Linux
- **Python**: 3.11.11 or higher
- **RAM**: Negligible (all LLM calls are made to an API)

---

## **Option 1: Local Installation (Recommended)**

### Step 1: Clone the Repository
```bash
git clone https://github.com/ividal/robustness-scans.git
cd robustness-scans
```

### Step 2: Install uv Package Manager

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

### Step 3: Set Up Python Environment
```bash
uv python install 3.11.11
uv venv
uv sync
```

### Step 4: Run the Vulnerability Scan
```bash
uv run python src/blueprint/manual_probe.py
```

This will:
- Load the IPCC climate change report
- Create a Q&A chatbot using the report
- Run vulnerability scans using Giskard
- Generate reports in HTML, JSON, and Markdown formats

The reports will be saved in the `outputs/` directory.

---

## **Option 2: Docker Installation**

### Step 1: Build the Docker Image
```bash
git clone https://github.com/ividal/robustness-scans.git
cd robustness-scans
docker build -t blueprint .
```

### Step 2: Run the Container
```bash
docker run -p 8501:8501 blueprint
```

### Step 3: Access the Application
Open your browser and navigate to http://localhost:8501

---

## **What's Next?**

Once you have the application running:

1. **Review the Reports**: Check the generated reports in the `outputs/` directory
2. **Understand the Results**: Analyze the vulnerability scan findings
3. **Customize the Tests**: Modify the scanning parameters for your specific use case
4. **Integrate with Your App**: Adapt the scanning tools for your own LLM application

For detailed information about the scanning process, see the **[Step-by-Step Guide](step-by-step-guide.md)**.
