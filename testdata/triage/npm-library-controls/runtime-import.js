const modulePromise = import('stream/web');
async function load() { return await import('stream/web'); }
const result = typeof import('stream/web');
