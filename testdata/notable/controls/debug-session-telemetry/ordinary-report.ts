function report(message: string, data: object) {
  const session = 'test-session';
  fetch('https://collector.example.test/ingest', {
    method: 'POST',
    headers: { 'X-Debug-Session-Id': session },
    body: JSON.stringify({ sessionId: session, message, data }),
  });
}
