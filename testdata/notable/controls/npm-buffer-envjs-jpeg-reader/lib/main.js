const fs = require('fs');

function readJpegComment(imagePath) {
  const buffer = fs.readFileSync(imagePath);
  return buffer.includes(Buffer.from('metadata'))
    ? buffer.toString('utf8').slice(0, 128)
    : '';
}

module.exports = { readJpegComment };
