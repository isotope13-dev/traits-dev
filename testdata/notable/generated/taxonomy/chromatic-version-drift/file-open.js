import fs from 'fs';
fs.createWriteStream('build.log').on('open', () => console.log('ready'));
