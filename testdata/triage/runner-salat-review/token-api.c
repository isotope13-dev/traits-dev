/* Ordinary token operations alone do not establish theft or escalation. */
void duplicate(void) {
    OpenProcessToken();
    DuplicateTokenEx();
}
