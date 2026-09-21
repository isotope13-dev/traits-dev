// Core-js-style kebab-case internal requires (cf. feather-icons bundles):
// must never read as lodash, whose internals are camelCase (./_baseClone).
var arrayIncludes = require('./_array-includes');
var createProperty = require('./_create-property');
var toLength = require('./_to-length');

module.exports = function (list, value) {
  createProperty(list, 0, value);
  return arrayIncludes(list, value) && toLength(list.length) > 0;
};
