'use strict';
// Registers a native messaging host under the current user's registry hive.
const { execFileSync } = require('child_process');

function setUserRegistryValue(subkey, value) {
  const ps = `$ErrorActionPreference = 'Stop'
$hk = [uint32]2147483649
$k = '${subkey}'
function Reg($m, $a) { Invoke-CimMethod -Namespace root/default -ClassName StdRegProv -MethodName $m -Arguments $a }
[void](Reg 'CreateKey' @{ hDefKey = $hk; sSubKeyName = $k })
$r = Reg 'SetStringValue' @{ hDefKey = $hk; sSubKeyName = $k; sValueName = ''; sValue = $env:APP_VALUE }`;
  return execFileSync('powershell.exe', ['-NoProfile', '-NonInteractive', '-Command', ps],
    { encoding: 'utf8', env: { ...process.env, APP_VALUE: value } }).trim();
}

module.exports = { setUserRegistryValue };
