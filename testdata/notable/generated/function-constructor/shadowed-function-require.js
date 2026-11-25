const Function = require('./models/function');
function create(opts, ctx) {
  return new Function({ type: opts.type, functionName: opts.name }, ctx);
}
module.exports = { create };
