function fr(str) {
  return Buffer.from(str, 'base64').toString('utf-8');
}
module.exports = { fr };
