# Companion Lab: Building a Meal-Based Grocery List Generator Agent

## Lab Overview
This lab guides students through building a simple, practical agent that demonstrates core agent capabilities: memory, tool usage, and autonomous decision making. Students will create an agent that generates grocery shopping lists based on selected recipes.

## Learning Objectives
- Implement a basic agent architecture from first principles
- Configure short-term memory using an in-memory vector store
- Integrate tools as Python functions for the agent to use
- Implement a simple decision cycle for autonomous agent behavior
- Evaluate and improve agent performance

## Lab Requirements

### Environment
- Python notebook environment (AWS SageMaker or MyBinder compatible)
- Claude Sonnet 3.5 v2 via AWS Bedrock
- Basic Python libraries (no complex dependencies)

### Agent Specifications

**Task**: Generate a grocery shopping list based on selected meals from a predefined menu of recipes.

**Agent Flow**:
1. User selects 1-3 meals from a provided menu of 10 recipes
2. Agent determines all required ingredients
3. Agent checks what ingredients the user already has (via user input)
4. Agent creates an optimized shopping list of missing ingredients

**Tools**:
1. **Recipe Lookup Tool**: Retrieves ingredient lists for specific recipes from a JSON database
2. **List Optimizer Tool**: Combines duplicate ingredients and adjusts quantities

**Memory Implementation**:
- In-memory vector store to remember previously discussed ingredients and user preferences during the session

**Decision Points**:
1. Determining which ingredients are missing based on user input
2. Combining ingredient quantities across multiple recipes
3. Suggesting basic substitutions if the user mentions dietary restrictions

## Lab Outline

### Section 1: Introduction [Incomplete]
- Overview of agent architecture
- Introduction to the grocery list generator use case
- Lab objectives and workflow

### Section 2: Setting Up the Environment [Incomplete]
- AWS Bedrock configuration
- Required Python packages
- Loading the recipe database

### Section 3: Building the Agent's Memory [Incomplete]
- Implementing an in-memory vector store
- Creating embedding functions
- Storing and retrieving conversation context

### Section 4: Implementing Agent Tools [Incomplete]
- Creating the Recipe Lookup Tool
- Building the List Optimizer Tool
- Testing tools independently

### Section 5: Designing the Decision Cycle [Incomplete]
- Prompt engineering for the planning phase
- Executing tool calls based on plans
- Implementing reflection and iteration

### Section 6: Integrating Components [Incomplete]
- Combining memory, tools, and decision making
- Creating the main agent loop
- Handling user interactions

### Section 7: Testing and Evaluation [Incomplete]
- Testing with various recipe selections
- Evaluating memory retention
- Assessing decision quality

### Section 8: Extensions and Challenges [Incomplete]
- Adding dietary restriction handling
- Implementing budget constraints
- Creating a more sophisticated memory system

## Data Requirements
- JSON database of 10 simple recipes with ingredients and quantities
- No external data sources needed

## Deliverables
- Completed Python notebook with functioning agent
- Short reflection on agent capabilities and limitations
- Ideas for extending the agent functionality