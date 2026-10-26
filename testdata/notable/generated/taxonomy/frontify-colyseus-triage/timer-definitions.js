class ClockTimer { setTimeout(handler, time, ...args) { return {handler, time, args}; } setInterval(handler, time, ...args) { return {handler, time, args}; } }
const documentation = "setTimeout(callback, 25)";
// setInterval(callback, 50);
