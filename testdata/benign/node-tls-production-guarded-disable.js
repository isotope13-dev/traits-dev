// A user-selected self-signed/dev TLS relaxation that is refused in
// production: the NODE_ENV=production check returns before the env
// assignment can take effect.
function applyTlsPolicy() {
  if (process.env.PLATFORM_VERIFY_SSL !== "false") return;
  if (process.env.NODE_ENV === "production") {
    console.warn("Refusing PLATFORM_VERIFY_SSL=false in production — TLS verification stays enabled");
    return;
  }
  process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
}

module.exports = { applyTlsPolicy };
