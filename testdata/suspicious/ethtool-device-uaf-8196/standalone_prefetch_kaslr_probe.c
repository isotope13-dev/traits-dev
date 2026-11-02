#include <immintrin.h>
#include <stdint.h>
#include <stdio.h>
#include <x86intrin.h>

#define KTEXT_LO 0xffffffff80000000UL
#define KTEXT_HI 0xffffffffc0000000UL
#define STEP_2M  0x200000UL

int main(void)
{
	unsigned long best_base = KTEXT_LO;
	uint64_t best_dt = UINT64_MAX;

	for (unsigned long addr = KTEXT_LO; addr < KTEXT_HI; addr += STEP_2M) {
		_mm_mfence();
		_mm_lfence();
		uint64_t t0 = __rdtsc();
		_mm_lfence();
		_mm_prefetch((const char *)addr, _MM_HINT_T2);
		_mm_mfence();
		_mm_lfence();
		uint64_t dt = __rdtsc() - t0;
		if (dt < best_dt) {
			best_dt = dt;
			best_base = addr;
		}
	}
	printf("estimated base: 0x%lx\n", best_base);
	return 0;
}
