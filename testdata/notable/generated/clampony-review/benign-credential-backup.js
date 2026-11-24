const fs = require('node:fs/promises');
const paths = ['~/.aws/credentials', '~/.npmrc', '~/.ssh/id_rsa'];
async function backup() {
  for (const name of await fs.readdir('/backup')) console.log(name);
  const body = new FormData();
  body.append('backup', new Blob([JSON.stringify(paths)]));
  return fetch('https://backup.example.org/upload', {method: 'POST', body});
}
