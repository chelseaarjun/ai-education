export default async function handler(req, res) {
  if (req.method === 'POST') {
    res.status(200).json({ reply: 'Hello world from the chatbot API!' });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
} 