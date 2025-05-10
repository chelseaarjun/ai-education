# Prompt Engineering Guide
Module 2: Master the art and science of effective prompts

Welcome to this guide on prompt engineering! Today, you'll explore how to effectively communicate with artificial intelligence models like Claude and Amazon Bedrock to get the best possible results for your applications.
Prompt engineering is a crucial skill in the AI era. By the end of this lesson, you'll understand how to craft effective prompts that can help you build sophisticated AI applications, even without extensive programming knowledge.

## 1. Prompt Engineering Overview

<!-- Insert: ![Prompt Engineering Overview Diagram](../../../../assets/images/prompt-overview-diagram.svg) -->

### 1.1 What are Prompts?
A **prompt is** the input you provide to an AI system to elicit a specific output. Think of it as the interface between human intent and AI capability—**they're how we communicate what we want the model to do.**

In technical terms, a **prompt is a sequence of tokens (words, characters, or subwords) that provides context and instructions** to a language model.

**Simple Prompt:**
"What is machine learning?"

**More Detailed Prompt:**
"Explain machine learning to a high school student in 3 paragraphs, covering supervised learning, unsupervised learning, and reinforcement learning."

### 1.2 Why Prompt Engineering Matters
- **Precision**: Well-crafted prompts yield more accurate and useful outputs
- **Efficiency**: Better prompts reduce iterations and token usage, saving time and costs
- **Consistency**: Systematic prompting leads to more predictable results
- **Capability Unlocking**: Many advanced AI capabilities are accessible only through proper prompting

### 1.3 The Prompt Engineering Mindset
Successful prompt engineers think from both perspectives:

- As the **human**: What exact information or action do I need?
- As the **AI model**: What instructions and context will help it understand my intent?

This dual perspective helps bridge the gap between human expectations and how AI systems actually process information.

### 1.4 Anatomy of an Effective Prompt

<!-- Insert: ![Anatomy of a Prompt Diagram](../../../../assets/images/prompt-anatomy-diagram.svg) -->

An effective prompt consists of three essential components that work together to guide the model toward producing desired outputs:

1. **Task Requirements**: Clear instructions defining the specific action the model should perform.
   - Applies specific language by using precise action verbs and measurable success criteria
2. **Background Context**: Relevant information that helps the model understand the task's setting.
   - Applies specific language by including only pertinent details and avoiding unnecessary information
3. **Input/Output Structure**: The format of information provided and the expected response format.
   - Applies specific language by clearly defining the desired output structure with concrete examples

The positioning of these components matters significantly. Due to the "primacy-recency effect," models tend to pay more attention to information at the beginning and end of prompts, with content in the middle receiving less focus.

**Example Basic Prompt Structure:**
```
[TASK REQUIREMENTS]: Create a summary of the following customer feedback 
that highlights key issues and one positive aspect.

[BACKGROUND CONTEXT]: This feedback is from a user of our mobile banking app
who has been a customer for 3 years and primarily uses the deposit and transfer features.

[INPUT]: "The app keeps crashing when I try to deposit checks using my camera. 
Otherwise it's pretty good and I like the new transfer feature."

[OUTPUT STRUCTURE]: Provide a 2-sentence summary followed by bullet points 
for key issues and one positive aspect.
``` 