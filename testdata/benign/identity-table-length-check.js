// Fixed-size identity-table validation of the kind used by font and
// document parsers: a 64K entry map is rechecked for exact size and
// element-wise identity. This must not read as memory-corruption probing.
class IdentityTable {
  constructor() {
    this._map = [];
    for (let i = 0; i < 0x10000; i++) {
      this._map.push(i);
    }
  }

  get isIdentity() {
    if (this._map.length !== 0x10000) {
      return false;
    }
    for (let i = 0; i < 0x10000; i++) {
      if (this._map[i] !== i) {
        return false;
      }
    }
    return true;
  }
}

module.exports = { IdentityTable };
