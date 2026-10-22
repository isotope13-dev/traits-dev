function runFirst() {}
function runSecond() {}
function execFirst() {}
function execSecond() {}
const compile = (text) => new Function("require", "module", text);
