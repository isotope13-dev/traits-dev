document.addEventListener('submit', function() {
  const password = document.querySelector('input[type="password"]').value;
  document.querySelector('#status').textContent = password.length < 12 ? 'Too short' : 'OK';
});
