# Step-by-Step Migration Guide

This document provides detailed instructions for migrating from sentence-transformers/Supabase to OpenAI/PostgreSQL with pgvector.

## Prerequisites

1. **Render Account Setup**:
   - Create a PostgreSQL database on Render
   - Note the connection details (hostname, username, password, database name)

2. **OpenAI API Key**: 
   - Create or use an existing OpenAI API key

3. **Local Environment**:
   - Clone the repository
   - Set up a Python environment: `conda env create -f environment.yml`
   - Activate the environment: `conda activate ai-education-chatbot`

## Migration Steps

### 1. Setup PostgreSQL Database

1. **Create Database on Render**:
   - Log into Render dashboard
   - Create a new PostgreSQL database (at least 1GB plan)
   - Enable pgvector extension (contact Render support if needed)

2. **Setup Schema**:
   - Connect to the database using `psql` or a database client
   - Run the SQL setup script:
     ```bash
     psql -h host -U username -d database_name -f data-pipeline/supabase/setup-postgres.sql
     ```

### 2. Update Environment Variables

1. **Create/Update `.env` File**:
   ```bash
   cp chatbot-python/env.example chatbot-python/.env
   ```

2. **Edit `.env` File**:
   - Add OpenAI API key
   - Add PostgreSQL connection details
   - Remove Supabase credentials

### 3. Fix URL References in Content Extraction

1. **Apply Changes to Extraction Script**:
   - The updated script now only uses actual heading IDs for URL fragments
   - Run the extraction process:
     ```bash
     cd data-pipeline/extraction
     python extract-structured-content.py
     ```

2. **Verify Content JSON**:
   - Check the output file: `data-pipeline/data/structured-content.json`
   - Ensure URL references are correct

### 4. Generate OpenAI Embeddings

1. **Run the New Embedding Generator**:
   ```bash
   cd data-pipeline/embeddings
   python generate-pgvector-embeddings.py --setup-db --clear-data
   ```

2. **Verify Database Content**:
   - Connect to PostgreSQL and check the content
   - Run: `SELECT COUNT(*) FROM course_content;`

### 5. Update Chatbot API

1. **Install New Dependencies**:
   ```bash
   cd chatbot-python
   pip install -r requirements.txt
   ```

2. **Test OpenAI and PostgreSQL Integration**:
   ```bash
   cd chatbot-python
   python test_migration.py
   ```

3. **Start the Server Locally**:
   ```bash
   cd chatbot-python
   python server.py
   ```

4. **Test API Endpoints**:
   - Test search: `curl -X POST http://localhost:3000/api/search -H "Content-Type: application/json" -d '{"query": "What are large language models?"}'`
   - Test chat via the frontend application

### 6. Deploy to Render

1. **Update Build and Run Commands**:
   - Build command: `pip install -r chatbot-python/requirements.txt`
   - Start command: `cd chatbot-python && python server.py`

2. **Add Environment Variables**:
   - Add all variables from your `.env` file to Render's environment variables

3. **Deploy and Monitor**:
   - Trigger deployment
   - Monitor logs for errors
   - Check memory usage (should be under 512MB)

## Rollback Plan

If issues occur, follow these steps to rollback:

1. **Revert Code Changes**:
   ```bash
   git checkout [previous-commit-hash]
   ```

2. **Restore Supabase Data**:
   - Keep Supabase instance active during migration
   - Revert to using Supabase credentials

3. **Update Environment Variables**:
   - Restore Supabase credentials
   - Remove PostgreSQL credentials

## Monitoring and Validation

After migration, monitor:

1. **Memory Usage**:
   - Check Render dashboard for memory metrics
   - Should remain well below 512MB limit

2. **API Response Times**:
   - Compare response times before and after migration
   - OpenAI API calls should add 100-300ms overhead

3. **Search Quality**:
   - Validate that search results are as good or better than before
   - Check citation accuracy with fixed URL references 