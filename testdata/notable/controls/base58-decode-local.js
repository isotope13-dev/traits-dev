function decode(string) {
  return base58.decode(string);
}

module.exports = { decode };
