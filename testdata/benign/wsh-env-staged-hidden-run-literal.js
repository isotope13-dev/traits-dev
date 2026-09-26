// Static detection fixture. Never execute: decoded names are inert.
var sh = ActiveXObject;
var shell = new sh(dec("V1NjcmlwdC5TaGVsbA==", "k"));
var env = shell.Environment(dec("UHJvY2Vzcw==", "k"));
var chunks = ["QQ==", "Qg=="];
for (var i = 0; i < chunks.length; i++) {
  env("kEy9xQW4mZg7") = chunks[i];
}
var key = "secretkey";
var out = "";
for (var j = 0; j < chunks.length; j++) {
  out += String.fromCharCode(chunks[j].charCodeAt(j % key.length) ^ key.charCodeAt(j % key.length));
}
env("mP4vRt8wX2zQ") = WScript.ScriptFullName;
shell["Ru" + "n"](out, 0x41 - 0x41, ![]);
