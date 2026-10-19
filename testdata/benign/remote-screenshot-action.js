// Web-scraping SDK request shape: the "screenshot" action is a label in a
// request type sent to a scraping API, which screenshots a remote web page
// server-side. Nothing captures this machine's display.
const axios = require('axios');
const action = { type: "screenshot", fullPage: true };
axios.post('https://api.example.test/v1/scrape', { url: 'https://example.test', actions: [action] });
