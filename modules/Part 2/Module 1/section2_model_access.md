# Section 2: Model Access - AWS Bedrock Services
*Duration: 3 minutes*

## What It Is (45 seconds)

AWS Bedrock Model Access provides a unified API gateway to multiple foundation models from leading AI companies, without requiring you to manage model hosting, scaling, or infrastructure. Think of it as a "model marketplace" where you can access Claude, Amazon Nova, Meta Llama, and other state-of-the-art models through standardized APIs.

**Core Concept**: Instead of deploying and managing individual models on your own infrastructure, you make API calls to pre-hosted, enterprise-ready foundation models that AWS maintains and scales automatically.

## Key Features (45 seconds)

### Model Types Available
AWS Bedrock provides different model types based on output modality:
- **Text Generation Models**: Claude, Nova, Llama for conversational AI and content creation
- **Image Generation Models**: Stability AI models for creating visual content  
- **Embedding Models**: Amazon Titan Embeddings, Cohere Embed for vector representations
- **Multimodal Models**: Nova models that can process both text and images

### API Interaction Patterns
```python
import boto3

# Basic text completion
bedrock_runtime = boto3.client('bedrock-runtime')

# Synchronous invoke
response = bedrock_runtime.invoke_model(
    modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": "Analyze this contract..."}]
    })
)

# Streaming for real-time responses
response = bedrock_runtime.invoke_model_with_response_stream(
    modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
    body=json.dumps({...})
)
```

## Benefits (45 seconds)

### Managed Infrastructure
- **Zero Infrastructure Management**: No EC2 instances, containers, or GPU clusters to manage
- **Auto-scaling**: Handles traffic spikes automatically without capacity planning
- **High Availability**: Built-in redundancy across AWS availability zones
- **Global Edge**: Low-latency access from multiple AWS regions

### Enterprise Security & Compliance
- **Encryption**: API requests and responses encrypted in transit and at rest with AWS KMS
- **VPC Support**: Private network access for sensitive workloads
- **Compliance**: SOC, HIPAA, GDPR compliance built-in

### Model Variety & Standardization
- **Consistent API**: Same boto3 patterns work across different model providers
- **Easy Model Switching**: Change `modelId` parameter to test different models
- **Version Management**: Access specific model versions for reproducible results

## Limitations & Considerations (45 seconds)

### Model Availability & Regional Constraints
- **Regional Limitations**: Not all models available in every AWS region
- **Model Deprecation**: AWS may retire older model versions with notice
- **Access Requests**: Some models require requesting access before use
- **Quota Limits**: Default rate limits may require adjustment for high-volume applications

### Pricing Models & Cost Considerations
**Two Primary Pricing Models**:

**1. On-Demand Pricing**:
- Pay-as-you-go with no time commitments
- Charged per input and output token processed
- Ideal for variable or unpredictable workloads
- Immediate access without capacity planning

**2. Provisioned Throughput Pricing**:
- Reserve guaranteed capacity measured in Model Units (MUs)
- Hourly billing with commitment options: no commitment, 1-month, or 6-month terms
- Longer commitments provide better hourly rates
- Required for custom fine-tuned models
- Better for large, consistent inference workloads

**3. Batch Processing**:
- 50% discount compared to on-demand pricing
- Submit large datasets as single input files
- Responses stored in S3 for later access

**Cost Optimization Strategies**:
- Use cheaper models (Nova, Llama) for simple tasks
- Implement token limits to prevent runaway costs  
- Cache responses for repeated queries
- Consider model switching based on complexity needs
- Monitor usage patterns to determine if provisioned throughput makes sense
- Use batch processing for large, non-time-sensitive workloads

### Control & Customization Limitations
- **Model Parameters**: Limited to provided configuration options
- **Custom Fine-tuning**: Only available for select models
- **Response Timing**: Can't control exact inference hardware or response times
- **Vendor Lock-in**: Switching to self-hosted requires significant architectural changes

### When Model Access Makes Sense
✅ **Good For**: Rapid prototyping, variable workloads, enterprise compliance needs, multi-model experimentation

⚠️ **Consider Alternatives When**: You need maximum cost control, custom model modifications, specific hardware requirements, or complete independence from cloud providers

## References

**AWS Bedrock Documentation**:
- [Supported Foundation Models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
- [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [Provisioned Throughput Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html)
- [Model Access Management](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html)
- [InvokeModel API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html)

---

*Next: How Bedrock Agents build on these foundation models to create autonomous AI workflows.*