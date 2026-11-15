const fs = require('fs');
const path = require('path');
const archiver = require('archiver');

function archiveProjectLocally() {
  const base = '/home/container';
  const output = fs.createWriteStream(path.join(base, 'tmp', 'support-bundle.zip'));
  const archive = archiver('zip');
  archive.pipe(output);
  archive.glob('**/*', {
    cwd: base,
    ignore: ['**/node_modules/**', '**/.git/**', '**/tmp/**']
  });
  archive.finalize();
}

module.exports = archiveProjectLocally;
