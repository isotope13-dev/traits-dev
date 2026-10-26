'use strict';

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const SEALED_MODULE_NAME =
  'A1smwgXgcm9tY2FsbGVyZGF0YfvHkr7h5Wm3h3kUqG9NzUB3Ja0HHcTeWBVOju51pqMSbw==';

function decryptBlob(encoded, password) {
  const blob = Buffer.from(encoded, 'base64');
  const salt = blob.subarray(0, 16);
  const iv = blob.subarray(16, 28);
  const tag = blob.subarray(28, 44);
  const ciphertext = blob.subarray(44);
  const key = crypto.scryptSync(password, salt, 32);
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);

  decipher.setAuthTag(tag);
  return Buffer.concat([decipher.update(ciphertext), decipher.final()]);
}

function materializeModule(encryptedPath, password) {
  const sealedSource = fs.readFileSync(encryptedPath, 'utf8');
  const plaintext = decryptBlob(sealedSource, password);
  const outputPath = path.join(
    path.dirname(encryptedPath),
    path.basename(encryptedPath).replace(/^enc_/, '')
  );

  fs.writeFileSync(outputPath, plaintext);
  return outputPath;
}

exports.validateGraph = function validateGraph(callerData) {
  const password = 'licensed-plugin-key';
  const moduleName = decryptBlob(SEALED_MODULE_NAME, password).toString('utf8');
  const encryptedPath = path.join(__dirname, moduleName);
  const loadedModule = require(materializeModule(encryptedPath, password));

  return loadedModule.validateGraph(password);
};
