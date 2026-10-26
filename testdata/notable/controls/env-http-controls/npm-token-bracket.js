module.exports = function registryConfigured() {
  return Boolean(process.env['NPM_TOKEN']);
};
