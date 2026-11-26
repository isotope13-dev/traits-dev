'use strict';
// Reads a registry default value through WMI without writing anything.
const { execFileSync } = require('child_process');

function readUserRegistryValue(subkey) {
  const ps = `$hk = [uint32]2147483649
$r = Invoke-CimMethod -Namespace root/default -ClassName StdRegProv -MethodName GetStringValue -Arguments @{ hDefKey = $hk; sSubKeyName = '${subkey}'; sValueName = '' }
$r.sValue`;
  return execFileSync('powershell.exe', ['-NoProfile', '-NonInteractive', '-Command', ps], { encoding: 'utf8' }).trim();
}

module.exports = { readUserRegistryValue };
