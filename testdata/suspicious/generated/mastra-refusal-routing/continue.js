const GATEWAY = "https://private.invalid/v1/chat/completions";
const CHAIN = ["private/first", "local/second"];
const SYS = "Summarize the supplied text.";
const DECLINES = ["I cannot", "I can't"];
async function scoreSubject(evidence, key) {
  for (const m of CHAIN) {
    const r = await fetch(GATEWAY, { method: 'POST',
      headers: { Authorization: 'Bearer ' + key, 'User-Agent': 'Mozilla/5.0' },
      body: JSON.stringify({ model: m, temperature: 0.2,
        messages: [{ role: 'system', content: SYS },
                   { role: 'user', content: JSON.stringify(evidence) }] }) });
    const txt = (await r.json()).choices[0].message.content;
    if (DECLINES.some(p => txt.includes(p))) continue;
    return txt;
  }
  return '';
}
