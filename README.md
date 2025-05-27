# AI Education: LLM Concepts & Prompt Engineering

☕️ **Enjoying the course?** If you like the course and want to support my work (I'm a coffee lover!), consider [buying me a coffee](https://buymeacoffee.com/arjunasoknair). Your support is greatly appreciated!

A comprehensive educational resource for learning about Large Language Models (LLMs) and effective prompt engineering techniques.

## Overview

This repository contains interactive web-based lessons designed to teach fundamental concepts about Large Language Models and prompt engineering. The materials are suitable for students, developers, and professionals looking to understand how LLMs work and how to effectively interact with them.

## Running the Part 1: Foundations Hands-On Lab Notebooks

You can run the labs in any of these environments. Follow the instructions for your preferred setup:

---

### 1. AWS SageMaker Studio

1. **Get the Course Files**
   - **Option A: If `git` is available**
     - Open a terminal in SageMaker Studio and run:
       ```bash
       git clone https://github.com/chelseaarjun/ai-education.git
       cd ai-education
       ```
   - **Option B: If `git` is not available**
     - Download the repository as a ZIP from GitHub ([Download ZIP](https://github.com/chelseaarjun/ai-education/archive/refs/heads/main.zip)).
     - Upload the ZIP file in the SageMaker file browser.
     - Extract it in a terminal:
       ```bash
       unzip ai-education-main.zip
       mv ai-education-main ai-education
       cd ai-education
       ```

2. **Install Dependencies**
   - In a terminal or notebook cell, run:
     ```bash
     pip install -r requirements.txt
     ```

3. **AWS Credentials**
   - SageMaker Studio usually has credentials pre-configured. If you need to override, set them in a notebook cell as shown below.

4. **Open the Notebooks**
   - Navigate to `lab/notebooks/` and open the desired notebook for your module.
---

### 2. MyBinder (Cloud, No Install Required)

1. **Launch Binder**
   - [Click this Binder link](https://mybinder.org/v2/gh/chelseaarjun/ai-education/HEAD?filepath=notebooks)

2. **Open the Notebooks**
   - In the Jupyter interface, navigate to `lab/notebooks/` and open the notebook for your module.

3. **Install Dependencies**
   - Dependencies are usually pre-installed, but you can run:
     ```bash
     pip install -r requirements.txt
     ```

4. **AWS Credentials**
   - Set your credentials in a notebook cell (see the setup section in each notebook):
     ```python
     import os
     os.environ['AWS_ACCESS_KEY_ID'] = 'YOUR_ACCESS_KEY'
     os.environ['AWS_SECRET_ACCESS_KEY'] = 'YOUR_SECRET_KEY'
     os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'  # or your region
     ```

---

### 3. Local Jupyter Notebook/Lab

1. **Install Git (if not already installed)**
   - **macOS:**
     ```bash
     brew install git
     ```
   - **Ubuntu/Linux:**
     ```bash
     sudo apt-get install git
     ```
   - **Windows:**
     Download and install from [git-scm.com](https://git-scm.com/).

2. **Get the Course Files**
   - **Option A: Using git**
     ```bash
     git clone https://github.com/yourusername/ai-education.git
     cd ai-education
     ```
   - **Option B: Without git**
     - Download the repository as a ZIP from GitHub ([Download ZIP](https://github.com/yourusername/ai-education/archive/refs/heads/main.zip)).
     - Extract the ZIP file:
       - **macOS/Linux (in terminal):**
         ```bash
         unzip ai-education-main.zip
         mv ai-education-main ai-education
         cd ai-education
         ```
       - **Windows:**
         - Right-click the ZIP file and select "Extract All..."
         - Or use a tool like [7-Zip](https://www.7-zip.org/)
         - Open the extracted `ai-education` folder

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Open Jupyter and the Notebooks**
   - Start Jupyter:
     ```bash
     jupyter notebook
     ```
   - In the Jupyter interface, navigate to `lab/notebooks/` and open the notebook for your module.

5. **AWS Credentials**
   - Set your credentials in a notebook cell (see the setup section in each notebook):
     ```python
     import os
     os.environ['AWS_ACCESS_KEY_ID'] = 'YOUR_ACCESS_KEY'
     os.environ['AWS_SECRET_ACCESS_KEY'] = 'YOUR_SECRET_KEY'
     os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'  # or your region
     ```

---

**Note on Data Files:**
- If you cloned or downloaded the full repository, all required data files (in `lab/data/`) are already present.
- If you only uploaded individual notebooks, you must also upload the `lab/data/` directory for the labs to work correctly.

---

**Tip:** For a fully cloud-based experience, use the [Binder link](https://mybinder.org/v2/gh/chelseaarjun/ai-education/HEAD?filepath=notebooks) to launch all notebooks in your browser—no installation required!

---

## Repository Structure

```
ai-education/
├── assets/
│   ├── css/           # Stylesheet files
│   ├── js/            # JavaScript files
│   └── images/        # Images and diagrams
├── pages/             # Individual lesson pages
└── index.html         # Main course homepage
```

## Contents

### 1. LLM Concepts
An in-depth exploration of how Large Language Models work, covering:

- **Context Windows**: Understanding token limitations and management
- **Tokenization**: How text is broken down for processing
- **Embeddings**: Semantic understanding and vector representations
- **Temperature & Sampling**: How models generate text responses
- **Response Formatting**: Structured vs. unstructured outputs
- **Model Selection**: Choosing the right model for your application

### 2. Prompt Engineering
A practical guide to crafting effective prompts, including:

- **Prompt Fundamentals**: Basic concepts and input-output relationships
- **Prompt Structure**: Instructions, context, examples, and output formats
- **Basic Techniques**:
  - Zero-shot, one-shot, and few-shot prompting
  - Role-based prompting
  - Constraint-based prompting
- **Advanced Techniques**:
  - Chain-of-thought prompting
  - Prompt chaining
  - ReAct (Reasoning and Acting)
  - RAG (Retrieval Augmented Generation)

### 3. Agents
A hands-on module on building LLM-powered agents, covering:

- **Agent Fundamentals**: What makes an agent, and how LLMs are extended with memory, tools, and decision cycles
- **When to Use Agents**: When prompt engineering is not enough
- **Memory, Tools, and Orchestration**: How agents reason, remember, and act
- **Agent Patterns**: Production considerations, error handling, and best practices

### 4. Model Context Protocol (MCP)
A developer-focused module on standardized AI integration:

- **MCP Architecture**: Host, client, and server roles
- **Message Types & Features**: JSON-RPC, tools, resources, prompts, and sampling
- **Connection Lifecycle & Security**: Session management, transport, and trust
- **SDKs & Extensibility**: Official SDKs for Python, TypeScript, and more

### 5. Open Source Tools
A comprehensive module on key open-source libraries and frameworks for building AI applications:

- **Core LLM Frameworks**: LangChain, LangGraph, LlamaIndex, CrewAI, FAISS, Unstructured, ModelContextProtocol, Langfuse
- **General Purpose Libraries**: FastAPI, Streamlit, Pydantic, Jinja2
- **Additional Libraries**: Ragas, DSPy, OpenLLMetry, Giskard, Guidance, Instructor, Supabase, Hugging Face Transformers, Ollama
- **Integration with AWS Bedrock**: Practical examples and best practices

## Features

- **Interactive Learning**: Quizzes, interactive demos, and simulated AI responses
- **Visual Explanations**: Diagrams and visual aids to explain complex concepts
- **Code Examples**: Practical implementation examples using Python and AWS Bedrock
- **Hands-on Practice**: Opportunities to craft and test different prompting strategies
- **Agent Orchestration**: Learn production agent patterns, error handling, and orchestration best practices
- **Security & Protocols**: Understand security, trust, and standardized integration with MCP
- **Companion Notebooks**: Jupyter notebooks for LLMs, prompt engineering, and agents

## Getting Started

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ai-education.git
   cd ai-education
   ```

2. Open the index.html file in your web browser:
   ```
   open index.html
   ```

3. Navigate through the lessons using the course navigation menu.

## Technical Requirements

- Modern web browser (Chrome, Firefox, Safari, or Edge)
- No server required - all lessons run client-side
- For code examples: Python 3.8+ with appropriate libraries (LangChain, Pydantic, etc.)

## Contributing

Contributions to improve the lessons or add new content are welcome! Please feel free to submit pull requests or open issues for discussion.

## License

This project is licensed under the terms of the included LICENSE file.

## Acknowledgments

- **AWS** for providing the Bedrock platform and Claude model access
- **Anthropic** for developing the Claude models referenced in the materials
- **LangChain** and **LangGraph** teams for their excellent frameworks
- **LlamaIndex**, **CrewAI**, **FAISS**, **Unstructured**, **Langfuse**, and **MLflow** teams for their open-source libraries and LLMOps tools
- **FastAPI**, **Streamlit**, **Pydantic**, **Jinja2**, and other Python open-source library authors for enabling modern AI application development
- **Hugging Face**, **DSPy**, **Ragas**, **OpenLLMetry**, **Giskard**, **Guidance**, **Instructor**, **Supabase**, **Ollama**, and the broader open-source AI community for their contributions and inspiration
- **Model Context Protocol** team for [protocol documentation and SDKs](https://modelcontextprotocol.io/)
- **Project Binder** for providing free cloud-based Jupyter notebook hosting
- All contributors, testers, and the open-source community for feedback and improvements

## Run All Companion Notebooks on Binder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/chelseaarjun/ai-education/HEAD?filepath=notebooks)

- Click the badge above to launch an interactive Jupyter environment in your browser (replace USERNAME/REPO with your GitHub repo).
- In the Jupyter interface, navigate to the `notebooks/` directory and open any companion notebook for the module you want to explore (e.g., `llm_companion.ipynb`).
- All required Python dependencies are pre-installed via `requirements.txt`.
- You will need to provide your own AWS credentials in the first cell of any notebook that uses Bedrock/Claude features.
---

Created with ❤️ for AI education and advancement.