# AI Education: LLM Concepts & Prompt Engineering

A comprehensive educational resource for learning about Large Language Models (LLMs) and effective prompt engineering techniques.

## Overview

This repository contains interactive web-based lessons designed to teach fundamental concepts about Large Language Models and prompt engineering. The materials are suitable for students, developers, and professionals looking to understand how LLMs work and how to effectively interact with them.

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

### 1. LLM Concepts Lesson
An in-depth exploration of how Large Language Models work, covering:

- **Context Windows**: Understanding token limitations and management
- **Tokenization**: How text is broken down for processing
- **Embeddings**: Semantic understanding and vector representations
- **Temperature & Sampling**: How models generate text responses
- **Response Formatting**: Structured vs. unstructured outputs
- **Model Selection**: Choosing the right model for your application

### 2. Prompt Engineering Lesson
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

### 3. Open Source Tools (Coming Soon)
An overview of key open-source libraries and frameworks for building AI applications:

- **Core LLM Frameworks**: LangChain, LlamaIndex, Langfuse
- **General Purpose Libraries**: FastAPI, Streamlit, Pydantic, Jinja2
- **Integration with AWS Bedrock**

## Features

- **Interactive Learning**: Quizzes, interactive demos, and simulated AI responses
- **Visual Explanations**: Diagrams and visual aids to explain complex concepts
- **Code Examples**: Practical implementation examples using Python and AWS Bedrock
- **Hands-on Practice**: Opportunities to craft and test different prompting strategies

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

## Using the Code Examples

The code examples in the lessons demonstrate integration with AWS Bedrock and Claude models. To run these examples:

1. Install required Python packages:
   ```
   pip install langchain boto3 pydantic jinja2
   ```

2. Configure AWS credentials for Bedrock access
3. Modify region and model parameters as needed for your environment

## Contributing

Contributions to improve the lessons or add new content are welcome! Please feel free to submit pull requests or open issues for discussion.

## License

This project is licensed under the terms of the included LICENSE file.

## Acknowledgments

- AWS for providing the Bedrock platform and Claude model access
- Anthropic for developing the Claude models referenced in the materials
- The LangChain team for their excellent framework

---

Created with ❤️ for AI education and advancement.