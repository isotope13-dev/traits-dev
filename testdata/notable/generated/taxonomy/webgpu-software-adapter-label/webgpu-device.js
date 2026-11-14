// Graphics library labels a software WebGPU adapter in its device info.
export function getDeviceInfo(adapterInfo, adapter) {
  const vendor = adapterInfo.vendor || 'unknown';
  const renderer = (adapterInfo.driver || '').split(' Version ')[0];
  const fallback = Boolean(adapterInfo.isFallbackAdapter ?? adapter?.isFallbackAdapter ?? false);
  const softwareRenderer = /SwiftShader/i.test(`${vendor} ${renderer} ${adapterInfo.architecture || ''}`);
  return {
    type: 'webgpu',
    vendor,
    renderer,
    gpu: softwareRenderer || fallback ? 'software' : 'unknown',
    gpuType: softwareRenderer || fallback ? 'cpu' : 'unknown'
  };
}
