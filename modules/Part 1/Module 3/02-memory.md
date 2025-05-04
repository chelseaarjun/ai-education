# Memory: Retaining and Utilizing Information

## What is Memory in AI Agents?

Memory enables an agent to remember, reason, and act based on past interactions, knowledge, and goals. For chatbots and digital agents, memory is essential for holding context, learning from conversations, and improving over time.

**Analogy:**  
Just as people remember recent conversations, facts, and how to perform tasks, agents use different types of memory to be helpful and context-aware.

---

## Memory Types in Language Agents

### 1. Working Memory

**Definition:**  
Working memory is the agent's "active desk"—it holds all the information the agent needs right now to make decisions and respond. This includes:
- The current user message and recent conversation history
- Any goals or tasks the agent is working on
- Facts or context retrieved from long-term memory for the current turn

**Key Points:**
- Working memory is refreshed every decision cycle (e.g., each time the agent responds)
- It is the main input to the LLM for generating a response
- After the LLM responds, new information (actions, decisions, updated goals) is stored back in working memory for the next cycle

**Analogy:**  
Like having all the notes and materials you need on your desk while working on a homework assignment—everything you need right now is in front of you and easy to use.

---

### 2. Long-Term Memory

Long-term memory is where the agent stores information it may need in the future, even after the current conversation or task is over. It has two main types:

| Type      | What it Stores                                 | Example in Chatbots/Agents                |
|-----------|-----------------------------------------------|-------------------------------------------|
| Episodic  | Specific experiences and events                | Past conversations, user preferences, previous actions taken |
| Semantic  | General knowledge and facts                    | Company policies, product info, FAQs, world knowledge |

- **Episodic memory** lets the agent recall what happened in previous chats or tasks.
- **Semantic memory** lets the agent look up facts or knowledge to answer questions or make decisions.

**Analogy:**  
Episodic memory is like your chat history or diary; semantic memory is like your personal wiki or knowledge base.

---

### 3. Procedural Memory

Procedural memory is how the agent knows what to do and how to do it.

- **Implicit procedural memory:** The skills and reasoning built into the LLM itself encoded in the model's weights.
- **Explicit procedural memory:** The agent's code, prompt templates, and programmed workflows (e.g., how to escalate a support ticket, how to call an API).

**Key Points:**
- Procedural memory is set up by the agent designer (the developer).
- It can be updated, but changes must be made carefully to avoid bugs or unintended behavior.

**Analogy:**  
Implicit is like knowing how to ride a bike; explicit is like following a recipe or checklist.

---

## How These Memories Work Together

- **Working memory** is the "hub" for each decision: it brings in the current message, retrieves relevant info from long-term memory, and uses procedural memory to decide what to do.
- **Episodic and semantic memory** are "archives" the agent can search for relevant past events or facts.
- **Procedural memory** is the "how-to manual" and skillset the agent uses to act.

---

### Memory Architecture Visualization

![Cognitive Agent Architecture](../../../assets/images/Cognitive%20Agent%20Architecture.png)

*This diagram shows how working memory, long-term memory (episodic and semantic), and procedural memory interact in a language agent. Working memory is the central workspace, connecting the agent's reasoning, actions, and memory systems.*

*Adapted from the CoALA framework. For more, see [Cognitive Architectures for Language Agents](https://arxiv.org/pdf/2309.02427).*

---

## Understanding Memory Implementation

### Retrieval-Augmented Generation (RAG) in Memory Access
RAG serves as a key pattern for integrating different types of memory:

1. **Working Memory Enhancement**
   - Retrieves relevant information from past memory
   - Incorporates procedural knowledge for task execution
   - Maintains coherent context during decision cycles

2. **Memory Flow**
   ```
   Task Input → Working Memory → Memory Access → Context Integration → Task Execution
   ```

---

## Practical Example (Chatbot Context)

**User:** "Last time I chatted, you gave me a troubleshooting tip. What was it?"

- **Agent's working memory:** Holds the current question and user ID.
- **Agent's episodic memory:** Retrieves the specific advice or troubleshooting tip given in the previous conversation with this user.
- **Agent's semantic memory:** Knows general troubleshooting procedures and device information.
- **Agent's procedural memory:** Uses a programmed workflow to guide the user through troubleshooting steps.

**Memory Type Breakdown:**
- **Episodic memory:** "In your last chat, I suggested you restart your router."
- **Semantic memory:** "Restarting the router is a common fix for connectivity issues."
- **Procedural memory:** The step-by-step process the agent uses to walk the user through restarting the router.

---

## Quiz

**Scenario:**  
A support chatbot helps users troubleshoot issues and remembers their preferences.

**Question:**  
Which memory type is used for:
1. Remembering the user's last support ticket?
2. Looking up the company's return policy?
3. Knowing how to guide a user through troubleshooting steps?

**Answers:**  
1. Episodic Memory  
2. Semantic Memory  
3. Procedural Memory

---

**Summary:**  
- **Working memory**: What the agent is thinking about right now
- **Episodic memory**: What the agent has experienced before
- **Semantic memory**: What the agent knows as facts
- **Procedural memory**: What the agent knows how to do 