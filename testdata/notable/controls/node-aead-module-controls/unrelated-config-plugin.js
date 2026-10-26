const fs = require('node:fs');
const crypto = require('node:crypto');
function openConfig(encoded, password) {
  const blob = Buffer.from(encoded, 'base64');
  const salt = blob.subarray(0, 16);
  const iv = blob.subarray(16, 28);
  const tag = blob.subarray(28, 44);
  const key = crypto.scryptSync(password, salt, 32);
  const cipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
  cipher.setAuthTag(tag);
  return JSON.parse(Buffer.concat([cipher.update(blob.subarray(44)), cipher.final()]));
}
function readConfig(filename, password) {
  return openConfig(fs.readFileSync(filename, 'utf8'), password);
}
function saveConfig(filename, json) { fs.writeFileSync(filename, json); }
function selectPlugin(serialized) {
  return JSON.parse(serialized).renderer === 'html' ? './html.js' : './text.js';
}
exports.load = function load(options) {
  const serialized = JSON.stringify(options);
  const plugin = require(selectPlugin(serialized));
  return plugin;
};
