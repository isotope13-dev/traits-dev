// handlebars SafeString: extending a class's own prototype is ordinary OOP,
// not a String.prototype extension for obfuscation.
function SafeString(string) {
  this.string = string;
}

SafeString.prototype.toString = SafeString.prototype.toHTML = function () {
  return '' + this.string;
};

module.exports = SafeString;
