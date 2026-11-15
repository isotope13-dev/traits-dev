const axios = require('axios');

const token = process.env.GITHUB_TOKEN;
const payload = { files: { 'notes.txt': { content: 'release notes' } } };
axios.post('https://api.github.com/gists', payload, {
  headers: { Authorization: `token ${token}` },
});
