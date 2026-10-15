// Genuine device-identity telemetry: qualified model fields paired with a
// brand, the shape device-brand-model-report-parameter still claims.
export async function reportDevice(host, info) {
  const url =
    host +
    "/ping?brand=" +
    encodeURIComponent(info.brand) +
    "&device_model=" +
    encodeURIComponent(info.deviceModel);
  await fetch(url, { method: "POST" });
}
