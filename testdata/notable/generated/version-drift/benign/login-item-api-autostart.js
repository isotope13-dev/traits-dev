// Benign control for xdg-persistence (stx triage): auto-launch goes
// through the OS-visible desktop helper API, the same shape as the Stacks
// desktop helper. The helper itself writes the entry; callers only invoke
// autoLaunch.enable/disable/isEnabled, which the composite excludes.
const appName = "ExampleApp";
function autostartDir() {
  return join(process.env.XDG_CONFIG_HOME || join(home(), ".config"), "autostart");
}
const entry = `[Desktop Entry]
Type=Application
Name=${appName}
Exec=${process.execPath}`;
async function enable() {
  if (!windowAvailable("autoLaunch")) return false;
  return await window.craft.autoLaunch.enable();
}
async function disable() {
  if (!windowAvailable("autoLaunch")) return false;
  return await window.craft.autoLaunch.disable();
}
async function isEnabled() {
  if (!windowAvailable("autoLaunch")) return false;
  return await window.craft.autoLaunch.isEnabled();
}
