function relaunchEditor(script) {
  return childProcess.spawn("powershell.exe", ["-WindowStyle", "Hidden", "-EncodedCommand", encode(script)]);
}
