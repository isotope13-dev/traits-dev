# WSH dropper vs daemon supervisor template controls

A connector daemon supervisor (excerpted from grix-connector's
`platform-adapter.js`) embeds `WScript.Shell` and
`Scripting.FileSystemObject` literals only inside VBS/PowerShell template
strings it generates for its own autostart watchdog, alongside an
`-ExecutionPolicy Bypass -EncodedCommand` launcher whose content is built
from visible plaintext lines in the same file. It never launches through
`Shell.Run` itself, so `wsh-powershell-dropper` must stay silent. A WSH
script that creates the hosts and `Run`s bypass PowerShell still convicts.

`cases.json` and `check.py` exercise both cases against ordinary Cleave
JSON analysis.

Run with:

```sh
python3 testdata/taxonomy/wsh-dropper-supervisor/check.py --cleave cleave
```
