# OpenAI + Supabase Migration Plan

This document outlines the plan for migrating the AI Education chatbot from sentence-transformers to OpenAI embeddings while continuing to use Supabase.

## Current System Issues

1. **Memory Constraint**: Running out of 512MB memory on Render with sentence-transformers
2. **URL Citation Problems**: Incorrect URL fragment references (#) in content extraction

## Migration Strategy

1. **Keep Supabase but replace sentence-transformers with OpenAI embeddings**
2. **Fix URL fragment reference issues in content extraction**

## Implementation Details

### 1. Update Content Extraction (`extract-structured-content.py`)

- Fix URL fragment references:
  - Only use actual IDs from the HTML, not generated ones
  - Check element.get('id') exists before using in URL fragments
  - Only generate reference URLs for sections with valid IDs

```python
# Fix: Use heading ID if available, otherwise don't use URL fragment
if heading.get('id'):
    subsection_id = heading.get('id')
    section_url = f"{url}#{subsection_id}"
else:
    subsection_id = f"section-{i}"
    section_url = url  # No fragment if no ID exists
```

### 2. Create OpenAI Embeddings Generator (`generate-supabase-openai-embeddings.py`)

- Use OpenAI API for embedding generation
- Maintain compatibility with Supabase's pgvector
- Handle 1536-dimensional embeddings (vs previous 384)

```python
@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
def generate_embeddings(texts, batch_size=20):
    """Generate embeddings using OpenAI API with retries."""
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=texts
    )
    return [item.embedding for item in response.data]
```

### 3. Update Supabase Schema

- Update pgvector dimensions from 384 to 1536 for OpenAI

```sql
-- Update existing table schema
CREATE TABLE IF NOT EXISTS course_content (
    -- other columns remain the same
    embedding VECTOR(1536)  -- Updated from 384 to 1536
);

-- Update similarity search function
CREATE OR REPLACE FUNCTION match_course_content(
    query_embedding VECTOR(1536),  -- Updated from 384 to 1536
    -- other parameters remain the same
)
```

### 4. Update API Endpoints

- Remove sentence-transformers dependency
- Add OpenAI API for embedding generation
- Keep Supabase for storage and search

## Step-by-Step Migration

1. **Prepare Environment**:
   - Update requirements.txt and environment.yml
   - Add OpenAI API key to .env file
   - Ensure Supabase credentials are set

2. **Fix URL References**:
   - Apply changes to extract-structured-content.py
   - Run the extraction process to generate structured-content.json

3. **Update Supabase Schema**:
   - Backup existing data if needed
   - Run setup SQL to update the vector dimensions to 1536
   - Clear existing embeddings (they'll no longer match)

4. **Generate New Embeddings**:
   - Run the new embedding generator:
     ```bash
     cd data-pipeline/embeddings
     python generate-supabase-openai-embeddings.py --setup-db --clear-data
     ```

5. **Update API Code**:
   - Deploy updated search.py and chat.py files
   - Test with the test_openai_supabase.py script

6. **Verify Changes**:
   - Test API endpoints for proper functionality
   - Check memory usage (should be much lower without sentence-transformers)
   - Verify citation URLs are working correctly

## Benefits

1. **Memory Efficiency**:
   - No local ML model loading (saves ~500MB memory)
   - Minimal memory footprint on Render

2. **Improved Embeddings**:
   - Higher quality embeddings from OpenAI
   - 1536 dimensions vs previous 384 dimensions

3. **Accurate Citations**:
   - Fixed URL references using only actual HTML element IDs
   - No more made-up URL fragments

## Testing

Run the test script to verify integration:
```bash
cd chatbot-python
python test_openai_supabase.py
```

## Cost Considerations

- OpenAI Embeddings API: ~$0.0004 per 1K tokens
- For a typical course content of ~500KB text:
  - Initial embedding generation: ~$0.10
  - Ongoing query costs: ~$0.0001 per user query

## Rollback Plan

If issues occur:
1. Revert code changes
2. Return to sentence-transformers
3. Re-generate embeddings with the original dimensions 