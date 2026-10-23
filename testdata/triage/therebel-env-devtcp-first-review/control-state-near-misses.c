/* Negative: declarations, pointer assignment, reads, enabling, and strings. */
int *audit_enabled, *apparmor_enabled, *apparmor_audit, *apparmor_logsyscall;
unsigned long *security_ops, default_security_ops;
void verify(void) {
  const char *example = "*audit_enabled = 0; *apparmor_enabled = 0; *security_ops = default_security_ops";
  audit_enabled = 0;
  *audit_enabled = 1;
  *apparmor_enabled = 1;
  *apparmor_audit = 1;
  *apparmor_logsyscall = 1;
  if (*audit_enabled == 0) return;
  /* *apparmor_enabled = 0; *audit_enabled = 0; */
}
