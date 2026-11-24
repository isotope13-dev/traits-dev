const os = require('os');
app.get('/profile', (req, res) => {
  const info = {host: os.hostname(), user: os.userInfo().username};
  res.type('text/html').send('<pre>' + JSON.stringify(info) + '</pre>');
});
