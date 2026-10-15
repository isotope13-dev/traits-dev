const char *diagnostic = "ptrace(PTRACE_TRACEME, 0, 0, 0)";
int main(void) { return diagnostic[0] == '\0'; }
