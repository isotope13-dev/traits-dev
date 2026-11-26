// OpenMausBot agent server: account sign-in defaults.
const APP_NAME = "OpenMausBot";
const DEFAULT_COMPANION_CONTROL_PLANE_URL="https://accounts.openmausbot.com";
export function controlPlane() {
  return DEFAULT_COMPANION_CONTROL_PLANE_URL;
}
