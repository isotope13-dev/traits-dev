void entry(void) { __asm__ volatile("xorps %xmm0,%xmm0; movups %xmm0,(%rax); xorps %xmm0,%xmm0; movups %xmm0,16(%rax)"); }
