const axios = require('axios');
const API_URL = 'https://fixture-7f2a9.ngrok-free.app';
async function status(code, language) {
  return axios.post(`${API_URL}/health`, { status: code, locale: language });
}
