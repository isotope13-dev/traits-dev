import { execSync } from 'node:child_process';
function getKey() {
  return execSync('gcloud secrets versions access latest --secret=GOOGLE_AI_API_KEY', {encoding:'utf8'}).trim();
}
async function callGemini() {
  const apiKey = getKey();
  return fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini:generateContent?key=${encodeURIComponent(apiKey)}`, {method:'POST', body:JSON.stringify({contents:[]})});
}
