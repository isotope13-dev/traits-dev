; legitimate plugin import thunks (no proxy slots, no initializer).

bits 64
default rel

extern host_resolve_symbol
extern host_entry_a
extern host_entry_b

section .text

global plugin_entry_a
plugin_entry_a:
    jmp   qword [rel host_entry_a]

global plugin_entry_b
plugin_entry_b:
    jmp   qword [rel host_entry_b]
