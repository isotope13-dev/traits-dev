import https from 'https';
import fetch from 'node-fetch';
const agent = new https.Agent({ rejectUnauthorized: false });
export async function ready(url) {
  try { await fetch(url, { agent }); return true; }
  catch (error) { return false; }
}
