const axios = require('axios');

const token = 'ghp_0123456789abcdefghijklmnopqrstuvwxyz';
const payload = {
  files: {
    'audit_log.txt': { content: `Target platform: ${process.platform}` },
  },
};

axios.patch('https://api.github.com/gists/0123456789abcdef0123456789abcdef', payload, {
  headers: { Authorization: `token ${token}` },
});
