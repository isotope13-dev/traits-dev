// OpenMausBot-derived agent server: account sign-in defaults.
const APP_NAME = "OpenMausBot";
const DEFAULT_COMPANION_CONTROL_PLANE_URL="https://accounts.fork-host.example";
export function controlPlane() {
  return DEFAULT_COMPANION_CONTROL_PLANE_URL;
}
