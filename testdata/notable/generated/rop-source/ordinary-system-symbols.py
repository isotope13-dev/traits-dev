# Symbol table inspection does not serialize executable control flow.
symbols = {'pop_rdi_ret': 0x1234, 'write_rdi_rsi_ret': 0x4567, 'system_plt': 0x7890}
for name, address in symbols.items():
    print(name, address)
