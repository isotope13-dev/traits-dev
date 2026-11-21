import { Octokit } from '@octokit/rest';
import fetch from 'node-fetch';

const octokit = new Octokit({ auth: 'ghp_7nK4pQ9vB2mR6xT3cY8dF5jH1wL0sZ4aE9uN' });
const owner = 'example-owner';
const repo = 'access-list';
const pathGit = 'Login.json';

async function register(number) {
  const { ip } = await (await fetch('https://api.ipify.org?format=json')).json();
  const record = { nomor: `${number}@s.whatsapp.net`, ip };
  const { data } = await octokit.repos.getContent({ owner, repo, path: pathGit });
  const records = JSON.parse(Buffer.from(data.content, 'base64').toString());
  records.push(record);
  await octokit.repos.createOrUpdateFileContents({ owner, repo, path: pathGit, content: JSON.stringify(records) });
}

export { register };
