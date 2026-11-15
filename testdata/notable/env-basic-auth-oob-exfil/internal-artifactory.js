const username = process.env.CAAS_ARTIFACTORY_READER_USERNAME || '';
const password = process.env.CAAS_ARTIFACTORY_READER_PASSWORD || '';
const auth = Buffer.from(`${username}:${password}`).toString('base64');
fetch('https://packages.example.internal/artifactory/api/go/golang-main/@v/list', {
  method: 'GET',
  headers: { Authorization: `Basic ${auth}` }
});
