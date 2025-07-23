# Customization Guide

This guide explains how to customize the Robustness Scans toolkit to fit your specific LLM application and testing needs.

---

## **Overview**

The Robustness Scans toolkit is designed to be highly customizable. You can adapt it for:
- Different PDF documents and sources
- Custom prompt templates
- Different LLM providers (Mistral AI or local Llamafile)
- Specific use cases and domains
- Custom test questions and datasets

---

## **Customizing the LLM Backend**

### **Using Different LLM Providers**

The toolkit supports multiple LLM providers through Langchain integrations:

#### **Mistral AI Models (Default)**
```python
from blueprint.chatbot import Chatbot
from blueprint.settings import IPCC_REPORT_URL, PROMPT_TEMPLATE, OUTPUT_FOLDER

chatbot = Chatbot(
    pdf=IPCC_REPORT_URL,
    prompt_template=PROMPT_TEMPLATE,
    local=False,  # Uses Mistral AI
    output_folder=OUTPUT_FOLDER
)
```

#### **Local Models with Llamafile**
```python
from blueprint.chatbot import Chatbot

chatbot = Chatbot(
    pdf="path/to/your/document.pdf",
    prompt_template="Your custom prompt template",
    local=True,  # Uses local Llamafile
    output_folder=OUTPUT_FOLDER
)
```

#### **Custom Llamafile Configuration**
```python
from blueprint.llamafile_chatbot import create_llamafile_chain

chain = create_llamafile_chain(
    llamafile_url="http://localhost:8080/v1",
    document_path="path/to/your/document.pdf",
    serialised_embeddings=None
)
```

---

## **Customizing Document Processing**

### **Using Different PDF Documents**

The toolkit can be adapted to work with different PDF documents:

#### **Custom PDF Document**
```python
# Modify the PDF path in your code
chatbot = Chatbot(
    pdf="path/to/your/custom_document.pdf",
    prompt_template=PROMPT_TEMPLATE,
    local=False
)
```

#### **Modifying Settings**
You can update the settings in `src/blueprint/settings.py`:
```python
# Change the default document
IPCC_REPORT_URL = "https://your-custom-document-url.pdf"

# Or use a local file
IPCC_REPORT_URL = "path/to/local/document.pdf"
```

### **Custom Prompt Templates**

Create custom prompts for your specific use case:

```python
# Define your custom prompt template
CUSTOM_PROMPT_TEMPLATE = """You are a helpful AI assistant.
Your task is to answer questions based on the provided context.
Please provide accurate and helpful answers.

Context:
{context}

Question:
{question}

Your answer:
"""

# Use it in your chatbot
chatbot = Chatbot(
    pdf="your_document.pdf",
    prompt_template=CUSTOM_PROMPT_TEMPLATE,
    local=False
)
```

---

## **Customizing Vulnerability Tests**

### **Adding Custom Test Questions**

Extend the vulnerability testing with your own test cases:

```python
from blueprint.manual_probe import create_mini_dataset
import pandas as pd
from giskard import Dataset

# Create custom test questions
custom_questions = [
    "Your custom test question 1",
    "Your custom test question 2",
    "Your custom test question 3"
]

# Create custom dataset
custom_dataset = Dataset(
    pd.DataFrame({"question": custom_questions}), 
    target=None
)
```

### **Domain-Specific Testing**

Create tests tailored to your specific domain:

```python
def create_domain_specific_dataset():
    """Create a dataset for your specific domain."""
    domain_questions = [
        "What are the key concepts in your domain?",
        "How does your system handle edge cases?",
        "What are the common failure modes?"
    ]
    
    return Dataset(
        pd.DataFrame({"question": domain_questions}), 
        target=None
    )
```

---

## **Customizing Report Generation**

### **Report Output Location**

Customize where reports are saved:

```python
from pathlib import Path

# Custom output directory
custom_output_folder = Path("custom_outputs")
chatbot = Chatbot(
    pdf="your_document.pdf",
    prompt_template=PROMPT_TEMPLATE,
    output_folder=custom_output_folder
)
```

### **Report Formats**

The system generates multiple report formats automatically:
- **HTML Reports**: Interactive web-based reports
- **JSON Reports**: Machine-readable data
- **Markdown Reports**: Human-readable summaries

All reports are saved to the specified output directory.

---

## **Integration with Existing Systems**

### **CI/CD Pipeline Integration**

Integrate vulnerability scanning into your deployment pipeline:

```yaml
# .github/workflows/vulnerability-scan.yml
name: Vulnerability Scan
on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      - name: Run vulnerability scan
        run: |
          uv run python src/blueprint/manual_probe.py
      - name: Upload scan results
        uses: actions/upload-artifact@v2
        with:
          name: scan-results
          path: outputs/
```

### **Custom Script Integration**

Create custom scripts to run scans:

```python
#!/usr/bin/env python3
"""Custom vulnerability scanning script."""

from blueprint.chatbot import Chatbot
from blueprint.manual_probe import create_mini_dataset
from giskard import Model, scan
from pathlib import Path

def run_custom_scan():
    """Run a custom vulnerability scan."""
    
    # Initialize chatbot with custom settings
    chatbot = Chatbot(
        pdf="path/to/your/document.pdf",
        prompt_template="Your custom prompt template",
        local=False,
        output_folder=Path("custom_outputs")
    )
    
    # Create custom dataset
    dataset = create_mini_dataset()
    
    # Wrap as Giskard model
    giskard_model = Model(
        model=chatbot.predict,
        model_type="text_generation",
        name="Custom Q&A Model",
        description="Your custom model description",
        feature_names=["question"]
    )
    
    # Run scan
    report = scan(giskard_model, dataset)
    
    # Generate reports
    report.to_html(filename="custom_outputs/scan_report.html")
    report.to_json(filename="custom_outputs/scan_report.json")
    report.to_markdown(filename="custom_outputs/scan_report.md")
    
    print("Scan completed! Check custom_outputs/ for results.")

if __name__ == "__main__":
    run_custom_scan()
```

---

## **Best Practices for Customization**

### **Configuration Management**
- Use constants in `settings.py` for configuration
- Create separate configuration files for different environments
- Document all custom configurations

### **Testing Customizations**
- Test with small datasets first
- Validate custom prompts work as expected
- Check that reports are generated correctly

### **Documentation**
- Document all custom configurations
- Provide examples for common use cases
- Maintain changelog for custom modifications

### **Performance Considerations**
- Use appropriate chunk sizes for document processing
- Consider using local models for sensitive data
- Monitor API usage when using cloud LLMs

---

## **Next Steps**

After customizing the toolkit for your needs:

1. **Test thoroughly** with your specific use cases
2. **Validate results** against known vulnerabilities
3. **Iterate and improve** based on findings
4. **Share improvements** with the community 