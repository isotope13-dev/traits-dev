fetch(origin).then(response => response.json()).then(record => {
  document.getElementById("status").textContent = record.status;
});
