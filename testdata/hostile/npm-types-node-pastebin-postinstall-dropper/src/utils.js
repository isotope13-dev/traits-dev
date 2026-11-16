module.exports = {
  b6: str => Buffer.from(str, 'base64').toString('utf-8'),
  rS: str => str.split('').reverse().join('')
};
