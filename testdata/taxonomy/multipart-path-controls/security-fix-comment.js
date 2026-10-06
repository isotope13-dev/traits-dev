// Security-fix comment quoting an encoded traversal payload as the hazard
// it prevents, not a path the code sends. Must not match
// micro-behaviors/fs/path/traversal::encoded-parent-dir-traversal.
// (Nodemailer documents its RFC 2231 continuation guard this way.)
function encodeContinuationSection(section) {
    // Decoding a literal section invents bytes that never appeared on the
    // wire: it is how the value 'filename*0*=utf-8''safe; filename*1=%2F..%2F..%2Fetc%2Fpasswd'
    // was emitted as a filename every receiving client reads back as
    // 'safe/../../etc/passwd'.
    return section.value.replace(/%/g, '=');
}
module.exports = { encodeContinuationSection };
