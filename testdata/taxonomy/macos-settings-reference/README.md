# macOS settings-app references

Static scanner inputs; no script is executed by the regression runner.

- `dialog.applescript`: a harmless dialog title names System Preferences.
- `settings.applescript`: ordinary activation of System Settings.
- `unrelated.applescript`: the same osascript capability without a settings name.

The first two retain neutral app-name and shell/osascript observations. None
should be suspicious or hostile. Bare names must not claim application automation.

Run from any directory:

```sh
python3 scripts/check-macos-settings-reference.py --cleave /path/to/cleave
```
