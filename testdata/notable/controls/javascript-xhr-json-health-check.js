const request = new XMLHttpRequest();
request.open("GET", "/health.json");
request.onreadystatechange = () => {
  if (request.readyState === 4 && request.status === 200) {
    const health = JSON.parse(request.responseText);
    document.querySelector("#status").textContent = health.status;
  }
};
request.send();
