module.exports = function registryConfigured() {
  return Boolean(process.env.NODE_AUTH_TOKEN);
};
