-- AI Education Vector Database Schema
-- For use with Supabase and pgvector

-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Course content table with vector support
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
    embedding VECTOR(384)
);

-- Links table
CREATE TABLE IF NOT EXISTS content_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID REFERENCES course_content(id) ON DELETE CASCADE,
    link_text TEXT,
    url TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE,
    is_reference BOOLEAN DEFAULT FALSE
);

-- Function for similarity search
CREATE OR REPLACE FUNCTION match_course_content(
    query_embedding VECTOR(384),
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

-- Index for faster vector search
CREATE INDEX IF NOT EXISTS course_content_embedding_idx ON course_content 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100); 