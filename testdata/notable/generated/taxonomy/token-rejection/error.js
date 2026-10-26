const fs = require('fs');
const os = require('os');
const timer = setInterval(async () => {
  const response = await fetch('https://api.github.com/user', {
    headers: {Authorization: 'Bearer ' + process.env.GITHUB_TOKEN}
  });
  if (response.status === 401) {
    throw new Error("invalid token");
    clearInterval(timer);
  }
}, 60000);
setTimeout(() => clearInterval(timer), 86400000);
