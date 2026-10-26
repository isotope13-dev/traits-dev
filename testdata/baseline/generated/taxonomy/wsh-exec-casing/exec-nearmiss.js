function parseVersion(output) {
  var fc = /v(\d+)\.(\d+)\.(\d+)/;
  var pc = /release-(\d+)/;
  var m = fc.exec(output) || pc.exec(output);
  return m && m[1];
}
