const alpha = n => String.fromCharCode(65+n);
const record = n => ({data:Buffer.alloc(n)});
const logPath = "worker.txt";
const cache = Math.random() < 0.1 ? "./config.json" : "";
function parent(path) { return path.length===1 || path.charCodeAt(0)===46; }
