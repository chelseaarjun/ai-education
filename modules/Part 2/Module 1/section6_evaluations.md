# Section 6: Evaluations

## 6.1 What it is 🎯

AWS Bedrock Evaluations is a comprehensive model performance testing and benchmarking service that enables teams to systematically assess foundation models and RAG applications before production deployment. Amazon Bedrock provides evaluation tools for you to accelerate adoption of generative AI applications. Evaluate, compare, and select the foundation model for your use case with Model Evaluation.

The service functions as your AI quality assurance platform, allowing you to:
- **Compare multiple foundation models** side-by-side using standardized metrics
- **Evaluate RAG systems** built with Knowledge Bases or custom implementations  
- **Test model outputs** against accuracy, robustness, and safety criteria
- **Generate detailed reports** with actionable insights for model selection

> 💡 **Production Context**: Think of Bedrock Evaluations as your "model testing lab" - test your AI models before deploying them to customer-facing applications.

---

## 6.2 Key Features 🛠️

### Automatic Evaluations
Automatic (Programmatic) model evaluation uses curated and custom datasets and provides predefined metrics including accuracy, robustness, and toxicity.

| Built-in Metric | Purpose | How It Works |
|---|---|---|
| **Accuracy** | Factual correctness | Uses BERT Score, F1 Score, or Real World Knowledge scores |
| **Robustness** | Response consistency | Tests model stability under prompt variations |
| **Toxicity** | Content safety | Detects harmful or inappropriate outputs using detoxify algorithm |

### Human Evaluations
Human evaluation workflows can use your own employees as reviewers or you can engage a team managed by AWS to perform the human evaluation.

**Two workforce options:**
- 🏢 **Your Own Team**: Use internal subject matter experts
- 🔧 **AWS Managed Team**: Professional evaluators managed by AWS

### LLM-as-a-Judge
You can also use an LLM-as-a-Judge to provide high quality evaluations on your dataset with metrics such as correctness, completeness, faithfulness (hallucination), as well as responsible AI metrics such as answer refusal and harmfulness.

### RAG Evaluation Capabilities
**Two evaluation types:**
1. **Retrieval Only**: Tests how well your Knowledge Base finds relevant information
2. **Retrieve and Generate**: Evaluates end-to-end RAG performance including response generation

---

## 6.3 Benefits 📈

### Integrated Evaluation Pipeline
Bedrock Evaluations seamlessly connects with other AWS Bedrock services you've already learned:

```
Prompt Management → Model Testing → Knowledge Base Evaluation → Agent Performance
      ↓                ↓                    ↓                       ↓
   Test prompts    Compare models    Validate retrieval    End-to-end testing
```

### Standardized Metrics Across Teams
- **Consistent benchmarking** ensures all team members use the same quality standards
- **Automated scoring** eliminates subjective bias in model comparisons
- **Built-in datasets** provide industry-standard baselines for common tasks

### Enterprise-Grade Features

| Feature | Business Value |
|---|---|
| **Compliance Tracking** | Maintain audit trails for model selection decisions |
| **Custom Metrics** | Define evaluation criteria specific to your grocery/retail use cases |
| **Source Attribution** | Track which data sources influenced model responses |
| **Integration APIs** | Embed evaluation into CI/CD pipelines |

### Cost-Effective Evaluation
You pay for the inferences that are performed during the course of the model evaluation, with no additional charge for algorithmically generated scores.

---

## 6.4 Limitations & Considerations ⚠️

### Evaluation Scope Constraints

**Supported Models**
- Limited to foundation models available in Amazon Bedrock
- Model evaluation jobs support using foundation models in Amazon Bedrock.
- External models require "bring your own inference" approach

### Custom Metric Limitations

| Limitation | Impact | Workaround |
|---|---|---|
| **JSON formatting requirements** | Complex metric definitions need careful structuring | Use provided templates and examples |
| **Variable constraints** | Limited placeholder variables for custom prompts | Plan evaluation templates carefully |
| **LLM judge dependencies** | Custom metrics rely on judge model capabilities | Test judge model selection thoroughly |

### Integration Requirements

**Data Preparation Overhead**
- Custom prompt datasets that you want to specify in the model evaluation job must have the required CORS permissions added to the Amazon S3 bucket.
- Ground truth datasets required for RAG evaluations
- JSONL format requirements for all evaluation datasets

**Performance Considerations**
- Evaluation jobs can take significant time for large datasets
- Human evaluations require coordination and scheduling
- Human-based evaluation with your own team, you pay for the inferences and $0.21 for each completed task.

### Production Planning Considerations

> ⚙️ **Implementation Reality Check**: Plan evaluation cycles into your development timeline - factor this into sprint planning.

**Key Questions to Consider/Ask**
1. Which evaluation metrics matter most for your specific use case?
2. Do you have sufficient domain expertise for human evaluations?
3. How will evaluation results influence your model selection process?
4. What's your tolerance for evaluation costs vs. quality assurance needs?
5. Do need ground truth dataset for evalution? 
---

## References

- [AWS Bedrock Evaluations Service Page](https://aws.amazon.com/bedrock/evaluations/)
- [Amazon Bedrock Documentation - Model Evaluation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html)  
- [AWS Blog: Amazon Bedrock Model Evaluation Generally Available](https://aws.amazon.com/blogs/aws/amazon-bedrock-model-evaluation-is-now-generally-available/)
- [AWS Machine Learning Blog: Custom Metrics in Bedrock Evaluations](https://aws.amazon.com/blogs/machine-learning/use-custom-metrics-to-evaluate-your-generative-ai-application-with-amazon-bedrock/)
- [AWS Machine Learning Blog: Knowledge Base Evaluations](https://aws.amazon.com/blogs/machine-learning/evaluating-rag-applications-with-amazon-bedrock-knowledge-base-evaluation/)