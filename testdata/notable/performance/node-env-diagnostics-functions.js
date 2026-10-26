function collectRuntimeConfig() {
  const runtime = process.version;
  const mode = process.env.APP_MODE;
  const region = process.env.DEPLOY_REGION;
  const endpoint = process.env.SERVICE_ENDPOINT;
  const retryLimit = process.env.RETRY_LIMIT;
  const logLevel = process.env.LOG_LEVEL;
  const cachePath = process.env.CACHE_PATH;
  const featureSet = process.env.FEATURE_SET;
  const tenant = process.env.TENANT_ID;
  const build = process.env.BUILD_ID;
  const diagnostic = { runtime, mode, region, endpoint, retryLimit, logLevel, cachePath, featureSet, tenant, build };
  return diagnostic;
}

function npmContext() {
  return process.env.npm_lifecycle_event;
}

function ciMarkers() {
  return process.env.CI;
}
