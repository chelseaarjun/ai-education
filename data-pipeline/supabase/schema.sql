-- AI Education Vector Database Schema
-- For use with Supabase and pgvector

-- Enable vector extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS vector;

-- Drop existing tables and functions
DROP TABLE IF EXISTS content_links;
DROP TABLE IF EXISTS course_content;
DROP FUNCTION IF EXISTS match_course_content;

-- Create course_content table with 1536 dimensions for OpenAI embeddings
CREATE TABLE IF NOT EXISTS course_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    url TEXT,
    content_type TEXT,
    part_id TEXT,
    module_id TEXT,
    parent_id UUID,
    importance REAL DEFAULT 0.7,
    embedding VECTOR(1536)
);

-- Create content_links table
CREATE TABLE IF NOT EXISTS content_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID REFERENCES course_content(id) ON DELETE CASCADE,
    link_text TEXT,
    url TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE,
    is_reference BOOLEAN DEFAULT FALSE
);

-- Create similarity search function for 1536 dimensions
CREATE OR REPLACE FUNCTION match_course_content(
    query_embedding VECTOR(1536),
    match_threshold FLOAT DEFAULT 0.5,
    match_count INT DEFAULT 5
)
RETURNS TABLE (
    id UUID,
    title TEXT,
    content TEXT,
    url TEXT,
    content_type TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        cc.id,
        cc.title,
        cc.content,
        cc.url,
        cc.content_type,
        1 - (cc.embedding <=> query_embedding) AS similarity
    FROM course_content cc
    WHERE 1 - (cc.embedding <=> query_embedding) > match_threshold
    ORDER BY similarity DESC
    LIMIT match_count;
END;
$$;

-- Create index for faster search
CREATE INDEX IF NOT EXISTS course_content_embedding_idx ON course_content 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Grant access to the Supabase service role
GRANT ALL ON TABLE course_content TO service_role;
GRANT ALL ON TABLE content_links TO service_role;
GRANT EXECUTE ON FUNCTION match_course_content TO service_role; 