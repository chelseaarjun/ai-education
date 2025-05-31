const fs = require('fs');
const path = require('path');
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error('Error: SUPABASE_URL and SUPABASE_KEY must be set in .env file');
  process.exit(1);
}

async function setupDatabase() {
  try {
    console.log('Connecting to Supabase...');
    const supabase = createClient(supabaseUrl, supabaseKey);
    
    // For pgvector extension, we'd need to use the SQL editor in Supabase dashboard
    console.log('NOTE: You need to enable the vector extension manually in the Supabase SQL Editor.');
    console.log('Run: CREATE EXTENSION IF NOT EXISTS vector;');
    
    // Create course_content table
    console.log('Creating course_content table...');
    const { error: tableError } = await supabase
      .from('course_content')
      .select('id')
      .limit(1)
      .catch(() => ({ error: { message: 'Table does not exist' } }));
    
    if (tableError) {
      console.log('Creating table structure...');
      // Here we should use the REST API to create tables
      // But for complex operations like creating vector columns,
      // it's better to use the SQL Editor in Supabase dashboard
    }
    
    console.log('Supabase setup needs to be completed manually.');
    console.log('Please copy the SQL from data-pipeline/supabase/schema.sql');
    console.log('and execute it in the Supabase SQL Editor.');
  } catch (error) {
    console.error('Error setting up Supabase:', error);
  }
}

setupDatabase();