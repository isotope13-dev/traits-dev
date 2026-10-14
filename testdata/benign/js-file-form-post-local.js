'use strict';
// Fixture: local files packed as multipart form data and POSTed to the
// caller-configured conversion endpoint (loopback). Same read + form +
// POST shape as the theft variant, but the destination is the local
// service the operator configured, not an OOB collector, so the
// file-form POST OOB composite must stay silent.
const fs = require('fs');
const FormData = require('form-data');

async function convertBundle(httpRequest, baseUrl, paths) {
  const form = new FormData();
  for (const filePath of paths) {
    const fileBuffer = fs.readFileSync(filePath);
    form.append('files', fileBuffer, { filename: 'bundle.bin' });
  }
  const url = `${baseUrl.replace(/\/$/, '')}/convert`;
  const response = await httpRequest({
    method: 'POST',
    url,
    body: form,
    returnFullResponse: true,
    headers: form.getHeaders()
  });
  return response;
}

module.exports = { convertBundle };
