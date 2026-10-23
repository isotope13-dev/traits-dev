void disable(int *audit_enabled, int *apparmor_enabled, int *apparmor_audit,
             int *apparmor_logsyscall, unsigned long *security_ops,
             unsigned long default_security_ops) {
 *audit_enabled = 0x00;
 *apparmor_enabled = 0U;
 *apparmor_audit = 0;
 *apparmor_logsyscall = 0L;
 *security_ops = default_security_ops;
}
