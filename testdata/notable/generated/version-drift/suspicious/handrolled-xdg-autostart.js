// True-positive control for xdg-persistence: a hand-written desktop
// entry dropped straight into the user autostart dir with a hard-coded
// payload path. No auto-launch API involved.
const fs = require("node:fs");
const os = require("node:os");
const entry = [
  "[Desktop Entry]",
  "Type=Application",
  "Name=Updater",
  "Exec=/tmp/.cache/updater --daemon",
  "Hidden=false",
].join("\n");
fs.writeFileSync(os.homedir() + "/.config/autostart/updater.desktop", entry);
