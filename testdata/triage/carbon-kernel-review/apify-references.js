const originalInit = Actor.init;
const originalOutput = Actor.pushData;
Actor.init();
Actor.pushData({ready: true});
Actor.init = function (...args) { return originalInit.apply(this, args); };
Actor.pushData = function (...args) { return originalOutput.apply(this, args); };
