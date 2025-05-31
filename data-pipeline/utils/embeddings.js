/**
 * Embeddings utility for generating vector embeddings from text
 * Uses @xenova/transformers for client-side embedding generation
 */
const { pipeline } = require('@xenova/transformers');

/**
 * SentenceTransformerEmbeddings class for generating embeddings
 * Uses the all-MiniLM-L6-v2 model from Xenova's transformers.js
 */
class SentenceTransformerEmbeddings {
  constructor(modelName = 'Xenova/all-MiniLM-L6-v2') {
    this.modelName = modelName;
    this.embeddingPipeline = null;
    this.embeddingDimension = 384; // Default for all-MiniLM-L6-v2
  }

  /**
   * Initialize the embedding model
   */
  async init() {
    if (!this.embeddingPipeline) {
      console.log(`Loading embedding model: ${this.modelName}`);
      try {
        // Set up caching to speed up subsequent loads
        process.env.TRANSFORMERS_CACHE = process.env.TRANSFORMERS_CACHE || './models';
        
        // Initialize the embedding pipeline
        this.embeddingPipeline = await pipeline('feature-extraction', this.modelName);
        console.log('Embedding model loaded successfully');
        return true;
      } catch (error) {
        console.error('Error loading embedding model:', error);
        throw error;
      }
    }
    return true;
  }

  /**
   * Generate embedding for a single text string
   * @param {string} text - The text to embed
   * @returns {Float32Array} - The embedding vector
   */
  async generateEmbedding(text) {
    if (!this.embeddingPipeline) {
      await this.init();
    }

    try {
      // Generate embedding
      const result = await this.embeddingPipeline(text, {
        pooling: 'mean',
        normalize: true
      });
      
      // Convert to array and return
      return Array.from(result.data);
    } catch (error) {
      console.error('Error generating embedding:', error);
      throw error;
    }
  }

  /**
   * Generate embeddings for multiple texts
   * @param {string[]} texts - Array of texts to embed
   * @returns {Float32Array[]} - Array of embedding vectors
   */
  async generateEmbeddings(texts) {
    if (!texts || texts.length === 0) {
      return [];
    }

    if (!this.embeddingPipeline) {
      await this.init();
    }

    try {
      // Process in batches for better efficiency
      const batchSize = 32;
      const embeddings = [];

      for (let i = 0; i < texts.length; i += batchSize) {
        const batch = texts.slice(i, i + batchSize);
        console.log(`Processing batch ${i / batchSize + 1}/${Math.ceil(texts.length / batchSize)}`);
        
        // Process batch sequentially to avoid OOM issues
        for (const text of batch) {
          const embedding = await this.generateEmbedding(text);
          embeddings.push(embedding);
        }
      }

      return embeddings;
    } catch (error) {
      console.error('Error generating embeddings:', error);
      throw error;
    }
  }
}

module.exports = {
  SentenceTransformerEmbeddings
}; 