const originalConsoleLog = console.log;
console.log = function (message) {
    originalConsoleLog(message);
    fetch('/log=harness-wasm-log.txt', {
        method: 'POST',
        body: ('stdout: ' + message),
        headers: { 'Content-Type': 'text/plain' }
    });
};
