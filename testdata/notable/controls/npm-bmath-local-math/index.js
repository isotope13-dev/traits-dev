function transform(number) {
  return String(number).split('').reverse().map(Number);
}

module.exports = { transform };
