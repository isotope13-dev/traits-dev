// Hostile control: a static blob piped through base64 into sh is a concealed
// payload, not transport -- no encoder call, nothing runtime. The
// decode-to-shell pipeline must still fire here.
const command = 'printf %s aGVsbG8gd29ybGQ= | base64 -d | sh';
