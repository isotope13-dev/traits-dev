#ifndef __VMLINUX_H__
#define __VMLINUX_H__
#pragma clang attribute push (__attribute__((preserve_access_index)), apply_to = record)
struct xdp_md { unsigned int data; };
#endif
#define SEC(name) __attribute__((section(name)))
SEC("xdp") int packet_filter(struct xdp_md *ctx) { return 0; }
char LICENSE[] SEC("license") = "GPL";
