const MODEL = "openai/private";
const endpoint = "/chat/completions";
// A refusal such as "I can't help with that" contains no observations.
function assertRecognizedObserverOutput(output, label, isRecognized) {
  if (!isRecognized(output.text)) throw new Error("no observations");
  return output;
}
async function observe(agent, messages) {
  for (let attempt = 0; attempt < 3; attempt++) {
    const output = await agent.stream(messages, { model: MODEL });
    try { return assertRecognizedObserverOutput(output, "Observer", parse); }
    catch (error) { if (attempt === 2) throw error; }
  }
}
