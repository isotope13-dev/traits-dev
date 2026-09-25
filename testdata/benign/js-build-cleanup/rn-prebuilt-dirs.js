'use strict';
// Build helper: refresh the prebuilt tree for the requested configuration.
const fs = require('fs');

const finalLocation = 'React-Core-prebuilt';

function replacePrebuiltConfiguration() {
  // Delete all directories - not files, since we want to keep the manifest file
  const dirs = fs
    .readdirSync(finalLocation, {withFileTypes: true})
    .filter(dirent => dirent.isDirectory());
  for (const dirent of dirs) {
    const dirPath = `${finalLocation}/${dirent.name}`;
    console.log('Removing directory', dirPath);
    fs.rmSync(dirPath, {force: true, recursive: true});
  }
}

module.exports = {replacePrebuiltConfiguration};
