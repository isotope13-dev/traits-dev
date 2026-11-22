function proxyRotator(config) {
  const { rotateOn = ['disconnect', 'network-error'] } = config;
  return { rotateOn };
}
function generateFingerprint(config = {}) {
  const { randomizeAppVersion = true, randomizeDeviceModel = true } = config;
  return { deviceModel: 'test', osVersion: '1', appVersion: [1, 0, 0] };
}
function applyFingerprint(config, fp) {
  config.browser = [fp.deviceModel, fp.osVersion, `WhatsApp/${fp.appVersion.join('.')}`];
  return config;
}
