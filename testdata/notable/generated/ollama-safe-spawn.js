import { spawnSync } from 'node:child_process';

export function chooseSense(entry, model, choices) {
  const prompt = buildPrompt(entry.sentence, entry.surface, choices);
  return spawnSync('ollama', ['run', model, '--ask', prompt], {
    input: entry.sentence,
    encoding: 'utf8',
    shell: false,
  }).stdout;
}
