#define _GNU_SOURCE
#include <immintrin.h>
#include <pthread.h>
#include <sched.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <x86intrin.h>

static void *bench_cache_worker(void *arg)
{
	char *arena = (char *)arg;
	cpu_set_t set;
	CPU_ZERO(&set);
	CPU_SET(0, &set);
	sched_setaffinity(0, sizeof(set), &set);

	uint64_t total = 0;
	for (size_t off = 0; off < 65536; off += 64) {
		_mm_mfence();
		_mm_lfence();
		uint64_t t0 = __rdtsc();
		_mm_prefetch(arena + off, _MM_HINT_T0);
		_mm_lfence();
		total += __rdtsc() - t0;
	}
	printf("prefetch cycles: %llu\n", (unsigned long long)total);
	return NULL;
}

int main(void)
{
	char *buf = calloc(1, 65536);
	if (!buf)
		return 1;
	pthread_t th;
	if (pthread_create(&th, NULL, bench_cache_worker, buf) == 0)
		pthread_join(th, NULL);
	free(buf);
	return 0;
}
