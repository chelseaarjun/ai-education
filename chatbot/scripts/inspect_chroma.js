/**
 * Script to inspect the ChromaDB database
 */
const { ChromaClient } = require('chromadb');
const path = require('path');
const fs = require('fs');

async function inspectChromaDB() {
  try {
    console.log("Inspecting ChromaDB...");
    
    // Path to the ChromaDB directory
    const chromaDbPath = path.join(__dirname, '..', 'data', 'chroma_db');
    console.log(`ChromaDB path: ${chromaDbPath}`);
    
    // Check if directory exists
    if (!fs.existsSync(chromaDbPath)) {
      console.error(`ChromaDB directory not found at: ${chromaDbPath}`);
      return;
    }
    
    // List the contents of the directory
    console.log("ChromaDB directory contents:");
    fs.readdirSync(chromaDbPath).forEach(file => {
      console.log(` - ${file}`);
      
      // If there's a subdirectory, list its contents too
      const subDirPath = path.join(chromaDbPath, file);
      if (fs.statSync(subDirPath).isDirectory()) {
        console.log(`   Contents of ${file}:`);
        fs.readdirSync(subDirPath).forEach(subFile => {
          console.log(`   - ${subFile}`);
        });
      }
    });
    
    // Try to read the SQLite database if it exists
    const sqlitePath = path.join(chromaDbPath, "chroma.sqlite3");
    if (fs.existsSync(sqlitePath)) {
      console.log(`SQLite database found at ${sqlitePath}`);
      console.log(`File size: ${(fs.statSync(sqlitePath).size / 1024 / 1024).toFixed(2)} MB`);
    }
    
    // Try to use the JavaScript client to initialize with file path
    try {
      console.log("Initializing ChromaDB client...");
      const client = new ChromaClient({
        path: "http://localhost:8000"
      });
      
      // Try to get a heartbeat
      console.log("Checking ChromaDB server heartbeat...");
      try {
        const heartbeat = await client.heartbeat();
        console.log(`ChromaDB heartbeat: ${heartbeat}`);
        
        // List collections
        console.log("Listing collections...");
        const collections = await client.listCollections();
        console.log("Collections:", collections);
        
        if (collections.length > 0) {
          // Get the first collection
          const collection = await client.getCollection({
            name: collections[0]
          });
          
          // Count items in the collection
          console.log(`Getting info for collection: ${collections[0]}`);
          const count = await collection.count();
          console.log(`Collection has ${count} items`);
          
          // Peek the collection
          console.log("Peeking the collection...");
          const peek = await collection.peek({ limit: 3 });
          console.log("Peek result:", JSON.stringify(peek, null, 2));
          
          // Try a query
          console.log("Querying the collection...");
          const queryResult = await collection.query({
            queryTexts: ["What are Large Language Models?"],
            nResults: 2
          });
          console.log("Query result:", JSON.stringify(queryResult, null, 2));
        }
      } catch (e) {
        console.error("Error connecting to ChromaDB server:", e.message);
      }
    } catch (e) {
      console.error("Error initializing ChromaDB client:", e.message);
    }
    
    console.log("Inspection complete");
  } catch (error) {
    console.error("Error during inspection:", error);
  }
}

// Run the inspection
inspectChromaDB(); 