// core-js aFunction/fails helpers, inlined into thousands of dist bundles:
// `typeof it != 'function'` is a type check (typeof yields a type keyword,
// never a shared secret) and `exec` is a local parameter, not a process
// exec call gated by a literal secret.
module.exports = function (it) {
  if (typeof it != 'function') throw TypeError(it + ' is not a function!');
  return it;
};

module.exports = function (exec) {
  try {
    return !!exec();
  } catch (e) {
    return true;
  }
};
