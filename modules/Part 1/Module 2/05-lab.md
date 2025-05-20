# Prompt Engineering Companion Lab: Plan

## Learning Objectives
By the end of this lab, you will be able to:
- Apply the CRISP framework to design effective prompts.
- Experiment with prompt structure, specificity, and context to influence model outputs.
- Use AWS Bedrock and Claude to test and refine prompts in real time.
- Practice iterative prompt refinement and compare outputs.
- Request and evaluate structured outputs from the model.
- Reduce hallucination and encourage self-evaluation in LLMs using advanced prompting techniques.

## Lab Sections

### A. Setup
- Install dependencies and configure AWS credentials (MyBinder/SageMaker compatible).
- Set the model ID at the top for reuse in all cells.

### B. Prompt Structure Exploration
- Input a simple prompt and observe the model's response.
- Try a more detailed prompt (add context, requirements, structure) and compare outputs.

### C. CRISP Framework in Action
- Fill in each CRISP element for a task.
- Assemble the full prompt and send to the model.
- Compare output to the simple prompt.

### D. Iterative Prompt Refinement
- Modify/refine the prompt based on model output.
- Re-run and compare results to see improvement.

### E. Structured Output Practice
- Request a structured (e.g., JSON) response for a task.
- Evaluate if the model follows the requested format.

### F. Hallucination, Self-Evaluation, and Multi-Path Reasoning
- **Hallucination Demo:** Try a prompt that encourages the model to make up information.
- **Self-Evaluation Prompting:** Use prompts that instruct the model to verify its answer or admit uncertainty.
- **Multi-Path Reasoning (Tree of Thoughts Lite):** Prompt the model to list multiple possible answers, evaluate each, and select the best one. Observe how this reduces hallucination and improves reliability.

### G. MyBinder & SageMaker Instructions
- Provide clear setup and compatibility notes for running the lab in both environments.

---

*This plan ensures students gain hands-on experience with prompt engineering concepts, practical prompt refinement, and advanced techniques for improving LLM reliability.* 