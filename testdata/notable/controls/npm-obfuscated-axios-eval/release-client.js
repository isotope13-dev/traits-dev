const axios = require('axios');

async function fetchReleaseInfo() {
  const response = await axios.get('https://updates.example.com/releases/latest');
  return response.data.version;
}

module.exports = { fetchReleaseInfo };
