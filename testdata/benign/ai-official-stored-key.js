import { readFileSync } from 'node:fs';
const config = JSON.parse(readFileSync('/home/example/.claude/settings.json', 'utf8'));
const token = config.env.ANTHROPIC_API_KEY;
const remote = 'https://api.anthropic.com';
fetch(`${remote}/v1/models`, { headers: { 'x-api-key': token } });
