// Mini-program runtime helper: branches on the host environment name.
function uploadTarget(options) {
  const host = getHostInfo();
  if ("miniprogram" === host().env) {
    return { filePath: options.filePath };
  }
  return { formData: options.formData, host: (__wxConfig.host || {}).env };
}
