// Installer trampoline deletes its temporary WSH script.
const cleanup = 'fso.DeleteFile(WScript.ScriptFullName)';
module.exports = cleanup;
