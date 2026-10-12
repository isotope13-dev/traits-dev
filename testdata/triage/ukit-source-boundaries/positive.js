import fs from 'node:fs';
import { spawnSync } from 'node:child_process';
const headers = {'api-key': token};
client.send('Runtime.evaluate', {expression: '1+1'});
const settings = path.join('Code', 'User', 'settings.json');
const directSettings = '/Library/Application Support/Code/User/settings.json';
async function download(url) {const res = await fetch(url); const body = await res.text(); fs.writeFileSync('out.txt', body);}
spawnSync('git', ['status']);
const policies = [{
  block: ['rm -rf /'],
  allow: ['git status']
}, {
  block: ['dd if=/dev/zero'],
  allow: ['git diff']
}];
