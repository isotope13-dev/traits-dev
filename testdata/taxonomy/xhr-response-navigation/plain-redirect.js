var xhr = new XMLHttpRequest();
xhr.open("GET", gateUrl);
xhr.onreadystatechange = function() {
  if (xhr.readyState === 4 && xhr.status === 200) {
    if (xhr.responseText === "ok") return;
    window.location.href = xhr.responseText;
  }
};
xhr.send();
