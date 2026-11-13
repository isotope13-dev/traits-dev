function report(message: string, data: object, hypothesisId: string) {
  const session = 'test-session';
  fetch('https://collector.example.test/ingest', {
    method: 'POST',
    headers: { 'X-Debug-Session-Id': session },
    body: JSON.stringify({
      sessionId: session,
      runId: 'test-run',
      location: 'estimator:offset',
      message,
      data,
      timestamp: Date.now(),
      hypothesisId,
    }),
  });
}
