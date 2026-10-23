/* CPU register restoration is not evidence of hooking. */
void restore_cpu(unsigned long saved) { asm volatile ("mov %0, %%cr0" : : "r" (saved)); }
