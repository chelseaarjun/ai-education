# Fundamentals of AI Agents

## What is an AI Agent?

An AI agent is a system that can perceive its environment, reason about it, and take actions to achieve specific goals—often autonomously. Agents have three essential components:

- **Tools:** Agents can use external tools (APIs, calculators, search engines) to extend their capabilities.
- **Memory:** Agents remember past actions, user preferences, or important facts (short-term and long-term).
- **Brain:** Agents use an LLM as their brain and repeat the Observe → Reason → Act loop as needed until an end state is reached.

## Traditional Workflows vs Prompt-Enhanced LLM Applications vs Agentic Applications

| Feature/Approach     | Traditional Workflow         | Prompt-Enhanced LLM Application      | Agentic Application                     |
|----------------------|-----------------------------|--------------------------------------|-----------------------------------------|
| Flexibility          | Rigid, fixed steps          | Flexible output, but fixed process   | Dynamic, adapts steps and tools         |
| Use of Tools         | Manual or pre-coded         | Limited (via prompt)                 | Can autonomously select and use tools   |
| Memory               | Minimal, often stateless    | Short-term (context window)          | Short-term and long-term, episodic, etc.|
| Reasoning            | Predefined logic            | LLM-based, but single-shot           | Multi-step, iterative, goal-driven      |

## Example: Document Extraction

- **Traditional Workflow:**  
  Extracts fixed fields from one type of document that always follows the same structure (e.g., always pulls "Name" and "Date" from a standard lease form).

- **Prompt-Enhanced LLM Application:**  
  Can flexibly extract different fields based on the prompt, but still processes one document at a time and does not adapt its process or use external tools.

  ```python
  from langchain.llms import Bedrock
  from langchain.prompts import PromptTemplate
  from langchain.chains import LLMChain

  # Initialize Bedrock LLM (replace with your model and credentials)
  llm = Bedrock(
      model_id="anthropic.claude-v2",  # or "amazon.titan-text-lite-v1"
      region_name="us-west-2"
  )

  # Define a prompt template for extracting fields
  prompt = PromptTemplate(
      input_variables=["document"],
      template="Extract the following fields from this lease document: Tenant Name, Lease Start Date, Rent Amount.\n\nDocument:\n{document}\n\nFields:"
  )

  # Create a simple LLM chain
  chain = LLMChain(llm=llm, prompt=prompt)

  # Example document
  doc = "This lease is made between John Doe and ACME Corp. Lease starts on 2024-07-01. Monthly rent is $2,500."

  # Run the chain
  result = chain.run(document=doc)
  print(result)
  ```

- **Agentic Application:**  
  Can interact with tools to translate documents, convert between different document types, and extract relevant fields—even adapting its approach based on the document's structure or missing information.

  ```python
  from langchain.llms import Bedrock
  from langchain.agents import initialize_agent, Tool
  from langchain.tools import BaseTool

  # Example tool: Document field extractor
  class FieldExtractorTool(BaseTool):
      name = "Field Extractor"
      description = "Extracts fields from a lease document."
      def _run(self, document: str):
          # (In practice, use an LLM or regex; here, just a placeholder)
          return "Tenant: John Doe, Start Date: 2024-07-01, Rent: $2,500"

  # Example tool: Translator
  class TranslatorTool(BaseTool):
      name = "Translator"
      description = "Translates a document to English."
      def _run(self, document: str):
          # Placeholder for translation logic
          return "Translated document: " + document

  # Initialize Bedrock LLM
  llm = Bedrock(
      model_id="anthropic.claude-v2",
      region_name="us-west-2"
  )

  # Register tools
  tools = [FieldExtractorTool(), TranslatorTool()]

  # Initialize agent
  agent = initialize_agent(
      tools=tools,
      llm=llm,
      agent_type="zero-shot-react-description"
  )

  # Example: Document in another language
  doc = "Este contrato de arrendamiento es entre John Doe y ACME Corp. Comienza el 1 de julio de 2024. La renta mensual es de $2,500."

  # Run the agent
  result = agent.run(f"Extract the tenant, start date, and rent from this lease document: {doc}")
  print(result)
  ```

## Quiz
**Question:**  
What is the primary difference between an LLM and an AI agent?
a) LLMs are less advanced than agents
b) Agents actively take actions and use tools to achieve goals
c) LLMs cannot understand human language
d) Agents do not use language models

**Scenario:**  
An agent receives a new sales report, analyzes the numbers to decide if inventory needs to be reordered, and then places an order if necessary.

**Question:**  
True or False: AI agents are always fully autonomous and require no human intervention.

A) True  
B) False  

Answer: False. Many agents operate with varying degrees of autonomy and may require human oversight or intervention at different points in their operation.
