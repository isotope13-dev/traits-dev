// Ordinary multi-provider router: falls back on transport errors only.
const ENDPOINT = 'https://openrouter.ai/api/v1/chat/completions';
const ROUTES = ['anthropic/claude-sonnet-4.5', 'openai/gpt-5.2', 'google/gemini-2.5-pro'];

async function summarize(text, key) {
  for (const model of ROUTES) {
    const res = await fetch(ENDPOINT, { method: 'POST',
      headers: { Authorization: 'Bearer ' + key },
      body: JSON.stringify({ model, messages: [
        { role: 'system', content: 'Summarize the document in three bullets.' },
        { role: 'user', content: text }] }) });
    if (res.status >= 500 || res.status === 429) continue;
    return (await res.json()).choices[0].message.content;
  }
  throw new Error('all providers unavailable');
}
module.exports = { summarize };
