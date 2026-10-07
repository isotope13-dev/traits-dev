function decode(text) {
  return text.replace(/\\u[0-9a-f]{4}/gi, function (match) {
    return String.fromCharCode(parseInt(match.slice(2), 16));
  });
}
let url = window.location.href;
url = url.replace(/\(/g, "\\(");
url = url.replace(/\)/g, "\\)");
