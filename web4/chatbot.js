const tf = require('@tensorflow/tfjs');
const use = require('@tensorflow-models/universal-sentence-encoder');
const readline = require('readline');

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

let model, embeddings = {};

// Load model
async function load() {
  model = await use.load();
  console.log("Model loaded");

  // Precompute embeddings
  for (let key in data) {
    embeddings[key] = await model.embed(data[key].examples);
  }

  startChat();
}

// Find best intent
async function getIntent(input) {
  const inputEmb = await model.embed([input]);

  let bestIntent = null;
  let bestScore = -1;

  for (let key in embeddings) {
    const scores = await tf.matMul(inputEmb, embeddings[key], false, true).data();
    const score = Math.max(...scores);

    if (score > bestScore) {
      bestScore = score;
      bestIntent = key;
    }
  }

  if (bestScore > 0.6) {
    return bestIntent;
  } else {
    return null;
  }
}

// Chat
function startChat() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  console.log("🤖 NLP Chatbot (type 'quit')");

  rl.on('line', async (input) => {
    if (input.toLowerCase() === 'quit') {
      console.log("Bye!");
      rl.close();
      return;
    }

    const intent = await getIntent(input);
    let reply;

    if (intent) {
      reply = data[intent].response;
    } else {
      reply = "I don't understand.";
    }

    console.log("Bot:", reply);
  });
}

// Start
load();