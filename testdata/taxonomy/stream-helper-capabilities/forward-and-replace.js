const raw = { log: console.log.bind(console) };
function emit(args) { raw.log(...args); }
console.log = () => {}; console.warn = () => {}; console.error = () => {};
