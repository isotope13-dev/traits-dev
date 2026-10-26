import https from 'https';
import fetch from 'node-fetch';
const agent = new https.Agent({ rejectUnauthorized: true });
export const ready = (url) => fetch(url, { agent });
