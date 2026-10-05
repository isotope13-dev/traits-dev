#include <linux/filter.h>
#include <linux/seccomp.h>
struct sock_filter filter[] = {
 BPF_STMT(BPF_LD | BPF_W | BPF_ABS, 0),
 BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 1, 0, 1),
 BPF_STMT(BPF_ALU | BPF_ADD, 0x10203040),
 BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW)
};

// A syscall (except filtered ones) is allowed.
