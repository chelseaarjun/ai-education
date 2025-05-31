-- pgvector setup script for Render PostgreSQL
-- Run this script to initialize the database schema for the AI Education chatbot

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Course content table with vector support for OpenAI embeddings (1536 dimensions)
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
    embedding vector(1536)
);

-- Links table for tracking references
CREATE TABLE IF NOT EXISTS content_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID REFERENCES course_content(id) ON DELETE CASCADE,
    link_text TEXT,
    url TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE,
    is_reference BOOLEAN DEFAULT FALSE
);

-- Function for similarity search with cosine distance
CREATE OR REPLACE FUNCTION match_course_content(
    query_embedding vector(1536),
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

-- Create vector search index
CREATE INDEX IF NOT EXISTS course_content_embedding_idx 
ON course_content 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Optional: Add helper functions for content management

-- Function to clear all data (for re-indexing)
CREATE OR REPLACE FUNCTION clear_course_content()
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM content_links;
    DELETE FROM course_content;
END;
$$;

-- Function to count indexed content
CREATE OR REPLACE FUNCTION count_indexed_content()
RETURNS TABLE (
    content_count BIGINT,
    links_count BIGINT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        (SELECT COUNT(*) FROM course_content) AS content_count,
        (SELECT COUNT(*) FROM content_links) AS links_count;
END;
$$; 