const axios = require('axios');
const API_URL = 'https://scan.example.invalid';
async function scan(code, language) {
  return axios.post(`${API_URL}/scan`, { code, language });
}
