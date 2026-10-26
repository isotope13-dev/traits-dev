fn inventory() { let present = (__cpuid(1).ecx & (1 << 31)) != 0; println!("{}", present); }
