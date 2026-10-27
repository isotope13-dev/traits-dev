# CAP_SYS_PTRACE is needed for the optional memory reader
setcap cap_sys_ptrace+ep "$MEMSCAN_PATH"
