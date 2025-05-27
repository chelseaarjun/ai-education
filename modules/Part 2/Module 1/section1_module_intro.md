# Section 1: Module Introduction - AWS Bedrock Services
*Duration: 1 minute*

Building directly on the foundational concepts from Part 1. You'll see how AWS implements the prompt engineering, agent patterns, and AI workflows you've learned about in a managed service environment.

This module covers core AWS Bedrock  service's capabilities, benefits, and limitations to help you understand what AWS offers for enterprise AI development.

## AWS Bedrock Service Ecosystem

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Model        │  │ Bedrock      │  │ Knowledge    │
│ Access       │  │ Agents       │  │ Bases        │
│              │  │              │  │              │
│ • Claude     │  │ • Action     │  │ • Unstructured: │
│ • Nova       │  │   Groups     │  │   S3, Web    │
│ • Llama      │  │ • Functions  │  │ • Structured:│
│              │  │ • Planning   │  │   Redshift,  │
│              │  │              │  │   Glue Data  │
│              │  │              │  │ • Vector:    │
│              │  │              │  │   OpenSearch,│
│              │  │              │  │   Aurora     │
│              │  │              │  │ • Hybrid:    │
│              │  │              │  │   Kendra     │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
  │ Guardrails   │ │ Prompt       │ │ Evaluations  │
  │              │ │ Management   │ │              │
  │ • Content    │ │              │ │ • A/B Tests  │
  │   Filters    │ │ • Versioning │ │ • Metrics    │
  │ • PII        │ │ • Templates  │ │ • Benchmarks │
  │   Detection  │ │ • Variables  │ │ • Human Eval │
  └──────────────┘ └──────────────┘ └──────────────┘
```

## What You'll Learn
AWS Bedrock provides the below six core managed AI services for building production-grade applications. We'll examine each Bedrock service systematically to build comprehensive understanding:

1. **Model Access** - Foundation model catalog and API patterns for LLM capabilities
2. **Bedrock Agents** - Autonomous AI workflows with reasoning and function calling  
3. **Knowledge Bases** - Managed RAG (Retrieval-Augmented Generation) for document integration
4. **Evaluations** - Performance testing and benchmarking for model quality assurance
5. **Prompt Management** - Version control and governance for prompt engineering workflows
6. **Guardrails** - Content filtering and safety controls for enterprise compliance

---

*Ready to explore AWS Bedrock's foundation model access? Let's start with the core of any AI application - getting LLM responses.*