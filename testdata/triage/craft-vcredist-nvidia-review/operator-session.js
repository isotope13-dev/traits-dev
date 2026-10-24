// Positive control for the pre-existing operator-session detector.
setInterval(async () => {
  const response = await fetch('session.php', {
    method: 'POST',
    body: JSON.stringify({action: 'ping', window_id: windowId, token: sessionToken})
  });
  const command = await response.json();
  if (command.redirect) window.location.href = command.redirect;
}, 3000);
