TEST(PtraceTest, SeizeInterruptGetRegSet) {
  const pid_t child_pid = fork();
  if (child_pid == 0) {
    while (1) {
    }
  }
  // Attach to the child with PTRACE_SEIZE; doing so should not stop the child.
  ASSERT_THAT(ptrace(PTRACE_SEIZE, child_pid, 0, 0), SyscallSucceeds());
  // Stop the child with PTRACE_INTERRUPT.
  ASSERT_THAT(ptrace(PTRACE_INTERRUPT, child_pid, 0, 0), SyscallSucceeds());
  struct iovec iov;
  EXPECT_THAT(ptrace(PTRACE_GETREGSET, child_pid, NT_PRSTATUS, &iov),
              SyscallSucceeds());
  EXPECT_TRUE(kill(child_pid, SIGKILL) == 0);
}
