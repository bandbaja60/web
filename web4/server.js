const express = require('express');
const cors = require('cors');
const tf = require('@tensorflow/tfjs');
const use = require('@tensorflow-models/universal-sentence-encoder');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Intents + responses
const data = {
  greeting: {
    examples: ["hi", "hello", "hey"],
    response: "Hello! How can I help you?"
  },
  goodbye: {
    examples: ["bye", "goodbye"],
    response: "Goodbye! 👋"
  },
  order: {
    examples: ["where is my order", "track order", "order status"],
    response: "Please provide your order ID."
  },
  thanks: {
    examples: ["thanks", "thank you"],
    response: "You're welcome!"
  }
};

let model;
let embeddings = {};

// Load model
async function loadModel() {
  model = await use.load();
  console.log("Model loaded");

  for (let key in data) {
    embeddings[key] = await model.embed(data[key].examples);
  }
}

// Find best intent
async function getIntent(input) {
  const inputEmbedding = await model.embed([input]);
  let bestIntent = null;
  let bestScore = -1;

  for (let key in embeddings) {
    const scores = tf.matMul(inputEmbedding, embeddings[key], false, true);
    const scoreValues = await scores.data();
    const maxScore = Math.max(...scoreValues);

    if (maxScore > bestScore) {
      bestScore = maxScore;
      bestIntent = key;
    }
  }

  return bestScore > 0.6 ? bestIntent : null;
}

// API endpoint
app.post('/chat', async (req, res) => {
  const { message } = req.body;
  const intent = await getIntent(message);
  const reply = intent ? data[intent].response : "I don't understand 🤔";
  res.json({ reply });
});

// Start server
loadModel().then(() => {
  app.listen(3000, () => console.log('🤖 Chatbot running on http://localhost:3000'));
});
