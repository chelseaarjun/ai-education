# Section 7: Guardrails

## 7.1 What it is 🛡️

AWS Bedrock Guardrails is a comprehensive safety and governance service that provides configurable safeguards for your generative AI applications based on your use cases and responsible AI policies. You can create multiple guardrails tailored to different use cases and apply them across multiple foundation models (FM), providing a consistent user experience and standardizing safety and privacy controls across generative AI applications.

Think of Guardrails as your AI application's "content moderation system" that automatically evaluates both user inputs and model responses to ensure they meet your organization's standards for safety, privacy, and appropriateness.

**Core Functions:**
- 🚫 **Content Filtering**: Block harmful content like hate speech, violence, or inappropriate material
- 🏷️ **Topic Management**: Prevent discussions of specific topics (e.g., investment advice for a banking chatbot)
- 🔒 **Privacy Protection**: Detect and mask personally identifiable information (PII)
- ✅ **Factual Accuracy**: Check responses against source material to reduce hallucinations

---

## 7.2 Key Features 🔧

### Content Filters
Amazon Bedrock Guardrails supports content filters to help detect and filter harmful user inputs and model-generated outputs in natural language.

| Content Category | What It Blocks | Adjustable Strength |
|---|---|---|
| **Hate** | Discriminatory language based on identity | Low, Medium, High |
| **Insults** | Demeaning, humiliating, or bullying language | Low, Medium, High |
| **Sexual** | Sexual content or inappropriate references | Low, Medium, High |
| **Violence** | Threats or glorification of physical harm | Low, Medium, High |
| **Misconduct** | Criminal activities or illegal content | Low, Medium, High |
| **Prompt Attack** | Jailbreak attempts and prompt injection | Low, Medium, High |

### Sensitive Information Filters
Amazon Bedrock Guardrails helps detect sensitive information, such as personally identifiable information (PIIs), in standard format in input prompts or model responses.

**Built-in PII Detection:**
- 🏠 Address, Age, Name, Phone numbers
- 💳 Credit card numbers, Bank account details, SSN
- 🆔 Driver's license, Passport numbers
- 📧 Email addresses, IP addresses

**Two Protection Modes:**
- **Block**: Reject entire requests containing sensitive information
- **Mask**: Replace PII with placeholders like `{NAME}` or `{CREDIT_CARD}`

### Advanced Safety Features

**Contextual Grounding Checks**
Guardrails supports contextual grounding checks to help detect and filter hallucinations if the responses are not grounded (for example, factually inaccurate or new information) in the source information and irrelevant to a user's query or instruction.

### Multi-Modal Protection
AWS Bedrock Guardrails includes image content filters that enable moderation of both image and text content in generative AI applications. The service can block up to 88% of harmful multimodal content.

---

## 7.3 Benefits 📊

### Industry-Leading Safety Protection
Guardrails provides comprehensive safety protections including text and image content safeguards that can block up to 88% of harmful multimodal content, and filters over 75% of hallucinated responses from models for Retrieval Augmented Generation (RAG) and summarization use cases.

### Integration with Other Bedrock Services

Guardrails automatically works with other AWS Bedrock services you've learned about in previous sections:

| Service Integration | How Guardrails Helps |
|---|---|
| **Model Inference** | Evaluates inputs and outputs during API calls to foundation models |
| **Agents** | Applies safety policies to multi-step agent workflows and tool calls |
| **Knowledge Bases** | Validates RAG responses against source material for accuracy |
| **Prompt Management** | Tests managed prompts against safety policies before deployment |

### Consistent Governance Across Models
A guardrail can be used with any text or image foundation model (FM) by referencing the guardrail during the model inference. You can use guardrails with Amazon Bedrock Agents and Amazon Bedrock Knowledge Bases.

| Benefit | Impact |
|---|---|
| **Model Agnostic** | Same safety policies across different foundation models |
| **Version Control** | Create versioned guardrail configurations for different environments |
| **Centralized Management** | Single location to manage all AI safety policies |
| **Cross-Region Support** | Automatic routing for optimal performance and availability |

### Cost-Effective Safety
AWS Bedrock Guardrails has significantly reduced pricing, with content filters now costing $0.15 per 1,000 text units and denied topics also at $0.15 per 1,000 text units. These recent price reductions make comprehensive AI safety more affordable for production deployments.

---

## 7.4 Limitations & Considerations ⚠️

### Language Support Constraints
Amazon Bedrock Guardrails supports English, French, and Spanish in natural language. Guardrails will be ineffective with any other language.

**Impact**: Multi-lingual applications need alternative safety measures for unsupported languages.

### Regional Availability
Amazon Bedrock Guardrails is primarily supported in US East (N. Virginia) and US West (Oregon) regions. However, cross-region inference capability now allows automatic routing of guardrail requests to optimal AWS regions within your geography (US, EU, APAC, GovCloud) for better performance and availability.

### Reasoning Model Limitations
Amazon Bedrock Guardrails doesn't support model reasoning with Anthropic Claude 3.7 Sonnet or DeepSeek-R1 when these models are operating in their "reasoning mode."

**What this means:**
- **Reasoning models** like Claude 3.7 Sonnet and DeepSeek-R1 can operate in two modes: standard output and step-by-step reasoning mode
- **Standard mode**: Guardrails work normally, evaluating both inputs and outputs
- **Reasoning mode**: Guardrails cannot inspect or filter the model's thinking process, only the final answer

**Impact**: Teams using reasoning models for complex problem-solving lose safety coverage during the intermediate reasoning steps, where models might generate inappropriate content that won't be detected by Guardrails.

### Performance and Cost Considerations

| Consideration | Impact | Mitigation Strategy |
|---|---|---|
| **Latency Addition** | Each guardrail evaluation adds processing time | Use selective evaluation and optimize policy combinations |
| **Per-Policy Pricing** | Costs accumulate with multiple active policies | Prioritize essential policies for production workloads |
| **False Positives** | Legitimate content may be blocked | Thoroughly test guardrail configurations with real data |

### Service Quotas and Scaling
AWS Bedrock Guardrails supports up to 50 calls per second using the ApplyGuardrail API (doubled from previous limits). Content filters, sensitive information filters, and word filters can process up to 200 text units per second (8x increase from previous limits).

### Production Planning Considerations

**Key Implementation Questions:**
1. **Which policies are essential vs. nice-to-have** for your specific use case?
2. **How will guardrail failures impact user experience** - graceful degradation vs. hard blocks?
3. **What's your strategy for handling false positives** in production?
4. **How will you test guardrail effectiveness** across diverse user inputs?

> ⚙️ **Implementation Reality Check**: Start with basic content filters and PII protection, then gradually add more sophisticated policies.

**Testing Strategy:**
- Use the built-in test window to validate configurations
- Create comprehensive test datasets representing real user interactions
- Monitor guardrail intervention rates in production
- Plan for periodic policy adjustments based on real-world usage

### Integration Dependencies
- **IAM Permissions**: Requires specific permissions for different guardrail policies
- **API Integration**: Applications need updates to handle guardrail responses
- **Monitoring Setup**: Tracking guardrail interventions requires additional observability

---

## References

- [AWS Bedrock Guardrails Service Page](https://aws.amazon.com/bedrock/guardrails/)
- [Amazon Bedrock Documentation - Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [AWS Blog: Guardrails for Amazon Bedrock Generally Available](https://aws.amazon.com/blogs/aws/guardrails-for-amazon-bedrock-now-available-with-new-safety-filters-and-privacy-controls/)
- [AWS Machine Learning Blog: Image Content Filters](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-guardrails-image-content-filters-provide-industry-leading-safeguards-helping-customer-block-up-to-88-of-harmful-multimodal-content-generally-available-today/)
- [AWS Documentation: Sensitive Information Filters](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-filters.html)
- [AWS Pricing: Bedrock Guardrails Pricing](https://aws.amazon.com/bedrock/pricing/)