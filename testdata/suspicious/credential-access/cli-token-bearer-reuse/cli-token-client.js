import { readFile } from 'node:fs/promises';
import { homedir } from 'node:os';
import { join } from 'node:path';

const CREDENTIALS = join(homedir(), '.config', 'example-cli', 'credentials.json');
const API_ORIGIN = 'https://api.example.com';

export async function fetchSiteIcon(id) {
  const stored = JSON.parse(await readFile(CREDENTIALS, 'utf8'));
  const accessToken = stored.credentials?.[API_ORIGIN]?.access_token;
  if (typeof accessToken !== 'string') return null;
  const response = await fetch(`${API_ORIGIN}/api/v1/apps/${encodeURIComponent(id)}/icon`, {
    headers: { authorization: `Bearer ${accessToken}` },
    redirect: 'manual',
  });
  return response.ok ? Buffer.from(await response.arrayBuffer()) : null;
}
