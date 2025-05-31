/**
 * Script to manually start ChromaDB server and test it's working
 */
const { spawn } = require('child_process');
const path = require('path');
const fetch = require('node-fetch');

// Path to ChromaDB data
const chromaDbPath = path.join(__dirname, '..', 'data', 'chroma_db');
console.log(`ChromaDB path: ${chromaDbPath}`);

// Command to start ChromaDB
const command = `python -m chromadb.cli.cli run --host localhost --port 8000 --path ${chromaDbPath}`;
console.log(`Starting ChromaDB server with command: ${command}`);

// Start ChromaDB server
const chromaServer = spawn('python', [
  '-m', 'chromadb.cli.cli',
  'run',
  '--host', 'localhost', 
  '--port', '8000',
  '--path', chromaDbPath
]);

// Log output
chromaServer.stdout.on('data', (data) => {
  console.log(`ChromaDB: ${data.toString().trim()}`);
});

chromaServer.stderr.on('data', (data) => {
  console.error(`ChromaDB Error: ${data.toString().trim()}`);
});

chromaServer.on('close', (code) => {
  console.log(`ChromaDB server exited with code ${code}`);
  process.exit(code);
});

chromaServer.on('error', (err) => {
  console.error('Failed to start ChromaDB server:', err);
  process.exit(1);
});

// Test connection after a delay
setTimeout(async () => {
  try {
    console.log('Testing connection to ChromaDB server...');
    const response = await fetch('http://localhost:8000/api/v1/heartbeat');
    if (response.ok) {
      console.log('✅ ChromaDB server is running!');
      const data = await response.text();
      console.log('Response:', data);
    } else {
      console.error('❌ ChromaDB server is not responding correctly, status:', response.status);
    }
  } catch (error) {
    console.error('❌ Failed to connect to ChromaDB server:', error.message);
  }
}, 5000);

console.log('ChromaDB server starting, press Ctrl+C to stop');

// Handle termination
process.on('SIGINT', () => {
  console.log('Shutting down ChromaDB server...');
  chromaServer.kill();
  process.exit(0);
}); 