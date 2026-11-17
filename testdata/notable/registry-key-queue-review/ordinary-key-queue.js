const QUEUE = [];
export function importKey(secretKey) { addToQueue(secretKey); }
function addToQueue(data) { QUEUE.push(data); }
fetch("https://rpc.example.net", { method: "POST", body: JSON.stringify({method: "getBalance"}) });
