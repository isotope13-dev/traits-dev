const DEBUG_SESSION = 'test-session';

function agentLog(message: string, data: object, hypothesisId: string) {
  fetch('https://collector.example.test/ingest', {
    method: 'POST',
    headers: { 'X-Debug-Session-Id': DEBUG_SESSION },
    body: JSON.stringify({
      sessionId: DEBUG_SESSION,
      runId: 'test-run',
      location: 'estimator:offset',
      message,
      data,
      timestamp: Date.now(),
      hypothesisId,
    }),
  });
}

function reportPosition(rssi: number, beaconX: number, beaconZ: number) {
  agentLog('position estimate', { rssi, beaconX, beaconZ }, 'estimate-1');
}
