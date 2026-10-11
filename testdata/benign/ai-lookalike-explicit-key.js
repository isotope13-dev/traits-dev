import { readFileSync } from 'node:fs';
const config = JSON.parse(readFileSync('/home/example/.claude/settings.json', 'utf8'));
const token = process.argv[2];
config.env.ANTHROPIC_API_KEY = token;
const remote = 'https://anthropic-gateway.example';
fetch(`${remote}/v1/models`, { headers: { 'x-api-key': token } });
