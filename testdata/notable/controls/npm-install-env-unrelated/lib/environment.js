// A local diagnostic returns names only, never credential values.
exports.secretNames = function secretNames() {
  return Object.keys(process.env).filter(name => /TOKEN|SECRET|KEY|NPM_/i.test(name));
};
