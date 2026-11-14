const theme = localStorage.getItem('theme');
fetch('/settings', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ theme })
});
