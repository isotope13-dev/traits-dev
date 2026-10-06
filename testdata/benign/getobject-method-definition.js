'use strict';

// Guards micro-behaviors/process/script/wsh::wsh-getobject-variable-argument:
// a JavaScript method *definition* named getObject must not read as a WSH
// GetObject moniker bind. Only the definition shape is present here; no WSH
// call exists in this file.
class ObjectStore {
  constructor() {
    this.cache = new Map();
  }

  async getObject(address) {
    return this.cache.get(address) || null;
  }

  async putObject(address, value) {
    this.cache.set(address, value);
  }
}

module.exports = { ObjectStore };
