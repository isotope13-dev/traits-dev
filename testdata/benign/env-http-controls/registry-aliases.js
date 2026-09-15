module.exports = function registryConfigured() {
  return Boolean(process.env.NPM_TOKEN || process.env.NODE_AUTH_TOKEN || process.env.NPM_AUTH_TOKEN);
};
