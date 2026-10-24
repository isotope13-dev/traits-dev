// Hash arithmetic and expression evaluation are unrelated capabilities.
function hash(text) { return text.charCodeAt(0) ^ text.charCodeAt(1); }
function calculate(expression) { return eval(expression); }
