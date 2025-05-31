/**
 * Test script to diagnose ChromaDB connection issues
 */
const { ChromaClient } = require('chromadb');
const fetch = require('node-fetch');

async function testChromaConnection() {
  console.log("Testing ChromaDB connection...");

  // Test direct HTTP access first
  try {
    console.log("\n1. Testing basic HTTP access to ChromaDB server...");
    const response = await fetch("http://localhost:8000/api/v1");
    console.log(`HTTP status: ${response.status}`);
    const data = await response.text();
    console.log("Response:", data.substring(0, 100) + (data.length > 100 ? "..." : ""));
    console.log("✅ Basic HTTP access successful");
  } catch (error) {
    console.error("❌ Basic HTTP access failed:", error.message);
    console.log("This suggests the ChromaDB server is not running or not accessible");
    return;
  }

  // Test ChromaClient
  try {
    console.log("\n2. Testing ChromaDB client initialization...");
    const client = new ChromaClient({
      path: "http://localhost:8000",
    });
    console.log("✅ ChromaDB client initialized");

    console.log("\n3. Testing heartbeat...");
    const heartbeat = await client.heartbeat();
    console.log("Heartbeat response:", heartbeat);
    console.log("✅ Heartbeat successful");

    console.log("\n4. Listing collections...");
    const collections = await client.listCollections();
    console.log("Collections:", collections);
    console.log(`✅ Found ${collections.length} collections`);

    if (collections.length > 0) {
      console.log("\n5. Testing access to first collection...");
      const collection = await client.getCollection({
        name: collections[0].name || collections[0]
      });
      console.log("Collection retrieved:", collection.name);
      
      console.log("\n6. Counting items in collection...");
      const count = await collection.count();
      console.log(`Collection contains ${count} items`);
      
      if (count > 0) {
        console.log("\n7. Peeking at collection data...");
        const peek = await collection.peek({limit: 1});
        console.log("Sample data:", JSON.stringify(peek, null, 2));
      }
    } else {
      console.log("\n5. Creating a test collection...");
      const testCollection = await client.createCollection({
        name: "test_collection",
        metadata: { description: "Test collection" }
      });
      console.log("Test collection created");
      
      console.log("\n6. Adding a test document...");
      await testCollection.add({
        ids: ["test1"],
        documents: ["This is a test document for ChromaDB connection testing."],
        metadatas: [{ source: "Connection Test" }]
      });
      console.log("✅ Test document added");
      
      console.log("\n7. Querying the test collection...");
      const results = await testCollection.query({
        queryTexts: ["test document"],
        nResults: 1
      });
      console.log("Query results:", JSON.stringify(results, null, 2));
    }
    
    console.log("\n✅ All ChromaDB connection tests passed!");
  } catch (error) {
    console.error("\n❌ ChromaDB connection test failed:", error);
    console.error("Error details:", error.stack);
  }
}

// Run the test
testChromaConnection().catch(console.error); 