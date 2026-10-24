// An XOR string reconstruction followed by actual evaluation must survive.
let script = "";
for (let i = 0; i < blob.length; i++) {
  script += String.fromCharCode(blob.charCodeAt(i) ^ 23);
}
eval(script);
