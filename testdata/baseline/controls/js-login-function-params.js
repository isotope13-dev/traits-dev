// A login handler whose parameters mention role names is not a credential
// collection: the weak-login-pair-set family must stay silent on function
// signatures and only fire on quoted-string collection literals.
const login = (id, userRole = 'guest') => check(id, userRole, 'admin');
