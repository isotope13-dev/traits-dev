const logger = { fork(label, fn) { return Promise.resolve().then(fn); } };
logger.fork('background-task', () => 42);
// A documentation example can say: fork('worker.js'); app.listen(3000);
const help = "log.fork('label', callback); server.listen(3000)";
export { logger, help };
