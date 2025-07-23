# **Step-by-Step Guide: How Vulnerability Scanning Works**

This guide walks you through the complete workflow of testing your LLM application for vulnerabilities using the Robustness Scans toolkit.

---

## **Overview**

The Robustness Scans system consists of several key components:

1. **Sample Q&A Application**: A Langchain-based chatbot that answers questions about climate change using the IPCC report
2. **Vulnerability Scanner**: Giskard-powered tools for detecting common LLM vulnerabilities
3. **Report Generation**: Generation of detailed scan reports in multiple formats

The system works by:
- Setting up a controlled test environment with a climate change Q&A chatbot
- Running various adversarial tests and probes using Giskard
- Analyzing responses for potential vulnerabilities
- Generating comprehensive reports with actionable insights

---

## **Step 1: Setting Up the Test Environment**

### **1.1 Sample Q&A Application**
The repository includes a sample Q&A chatbot built with:
- **Langchain**: For the core chatbot functionality using RetrievalQA
- **Langchain-Community**: For document loading and vector storage
- **PyPDF**: For parsing the IPCC PDF report
- **Mistral AI**: As the underlying LLM (via API)
- **FAISS**: For vector storage and similarity search

### **1.2 Configuration**
The application is configured through constants in `settings.py`:
- `IPCC_REPORT_URL`: URL to the IPCC climate change report
- `PROMPT_TEMPLATE`: Template for the climate assistant prompt
- `OUTPUT_FOLDER`: Directory for storing outputs and reports
- `SAMPLE_QA_PATH`: Path to sample Q&A dataset

---

## **Step 2: Running Vulnerability Scans**

### **2.1 Giskard Integration**
The system uses Giskard for vulnerability scanning:
- **Model Wrapping**: The chatbot is wrapped as a Giskard Model
- **Dataset Creation**: Test questions are organized into Giskard Datasets
- **Scan Execution**: Giskard's scan function runs comprehensive vulnerability tests

### **2.2 Scan Process**
The scanning process includes:
- **Hallucination Detection**: Tests if the LLM generates false information about climate change
- **Adversarial Testing**: Probes for various types of vulnerabilities
- **Robustness Assessment**: Evaluates how well the application handles different inputs

### **2.3 Test Data**
The system uses:
- **Sample Questions**: Pre-defined climate change questions for testing
- **Expected Answers**: Reference answers for comparison
- **Mini Dataset**: A small set of questions for quick testing

---

## **Step 3: Analyzing Results**

### **3.1 Scan Reports**
The system generates multiple report formats:
- **HTML Reports**: Interactive web-based reports (`scan_report.html`)
- **JSON Reports**: Machine-readable data (`scan_report.json`)
- **Markdown Reports**: Human-readable summaries (`scan_report.md`)

### **3.2 Report Location**
All reports are saved to the `outputs/` directory:
- `outputs/scan_report.html`
- `outputs/scan_report.json`
- `outputs/scan_report.md`

### **3.3 Understanding Results**
Reports include:
- Vulnerability scores and assessments
- Specific test cases that triggered issues
- Recommendations for improvement
- Detailed analysis of model behavior

---

## **Step 4: Customization and Integration**

### **4.1 Adapting to Your Application**
The scanning tools can be customized for:
- Different PDF documents (modify `IPCC_REPORT_URL`)
- Custom prompt templates (modify `PROMPT_TEMPLATE`)
- Different LLM providers (modify chatbot initialization)
- Specific use cases (modify test questions)

### **4.2 Local Model Support**
The system supports local models through Llamafile:
- Use `local=True` in Chatbot initialization
- Configure Llamafile endpoint URL
- Use local embeddings for document processing

### **4.3 Integration Examples**
```python
# Custom document
chatbot = Chatbot(
    pdf="path/to/your/document.pdf",
    prompt_template="Your custom prompt template",
    local=False
)

# Custom test questions
custom_questions = ["Your question 1", "Your question 2"]
dataset = Dataset(pd.DataFrame({"question": custom_questions}), target=None)
```

---

## 🎨 **Customizing the Scanning System**

To better understand how you can tailor the scanning parameters to suit your specific LLM application, please visit the **[Customization Guide](customization.md)**.
