// Chat analyzer: sends the chat transcript to the model provider.
const AI_KEY = 'sk-0123456789abcdefghijklmnopqrstuv';
const AI_URL = 'https://api.deepseek.com/v1/chat/completions';
async function analyzeWithAI(transcript) {
  const res = await fetch(AI_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + AI_KEY },
    body: JSON.stringify({ model: 'deepseek-chat', messages: [{ role: 'user', content: 'Analyze:\n' + transcript }] }),
  });
  return res.json();
}
