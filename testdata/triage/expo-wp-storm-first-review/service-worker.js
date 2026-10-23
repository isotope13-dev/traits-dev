export function send(worker, data) { worker.postMessage(JSON.stringify(data)); }
