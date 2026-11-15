const axios = require('axios');
const endpoint = 'https://fixture-7f2a9.ngrok-free.app/scan';
async function analyze(source, syntax) {
  return axios.post(endpoint, { language: syntax, code: source });
}
