const body = new FormData();
const file = new Blob(['ok']);
body.append('file', file, 'report.txt');
fetch('https://upload.example/files', {method: 'POST', body});
