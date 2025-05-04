# Brain: The Agent Loop

The agent loop is the core cycle that powers every AI agent:

- **Observe:**  
  The agent gathers and interprets information from various sources (e.g., user input, documents, APIs, sensors).

- **Reason:**  
  The agent determines the best course of action to achieve its assigned goal, using logic, rules, or learned strategies.

- **Act:**  
  The agent executes its decisions—this could mean generating a response, calling function or an API, updating a database etc.

---

## Visual: Circular Agent Loop

![Agent Loop Diagram](agent-loop.svg)

*Diagram description: Three nodes in a circle labeled Observe, Reason, and Act. Arrows connect them in a loop, with the labels "Plan" (Observe→Reason), "Execute" (Reason→Act), and "Access" (Act→Observe) next to the arrows.*

---

## Quiz

**Question:**  
Why is Claude 3.5 Sonnet better suited for agent development than earlier models?

A) It has a larger context window
B) It processes requests faster
C) It has enhanced reasoning capabilities for planning and tool use
D) It costs less to operate
Answer: Claude 3.5 Sonnet has improved reasoning capabilities that make it better at planning sequences of actions and using tools effectively, which are essential skills for powering agents.

**Scenario:**  
An agent receives a new sales report, analyzes the numbers to decide if inventory needs to be reordered, and then places an order if necessary.

**Question:**  
Which part of the agent loop is responsible for analyzing the numbers and deciding if inventory needs to be reordered?

A) Act  
B) Reason  
C) Stop  
D) Wonder  

**Correct Answer:**  
**B) Reason** 

---