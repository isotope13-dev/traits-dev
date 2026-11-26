// OpenMausBot-derived agent server: account sign-in defaults in a config object.
const APP_NAME = "OpenMausBot";
export const config = {
  CONTROL_PLANE_URL: 'https://id.fork-host.example',
};
export function controlPlane() {
  return config.CONTROL_PLANE_URL;
}
