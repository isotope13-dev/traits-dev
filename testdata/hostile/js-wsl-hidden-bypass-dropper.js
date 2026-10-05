// True-positive control for wsl-hidden-powershell-boundary-crossing:
// a WSL gate (distro-name check) launching hidden, policy-bypassed
// PowerShell with an encoded payload through child_process. No bundle
// identity, no helper context: the hostile composite must keep firing.
function crossIntoWindows(payloadB64) {
  if (!process.env.WSL_DISTRO_NAME) return;
  const args = ["-NoProfile", "-WindowStyle", "Hidden", "-ExecutionPolicy", "Bypass", "-EncodedCommand", payloadB64];
  require("node:child_process").execSync("powershell.exe " + args.join(" "));
}
module.exports = { crossIntoWindows };
