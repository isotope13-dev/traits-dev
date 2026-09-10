#include <elf.h>
#include <stdint.h>

/* A read-only format inspector; no file modification or entry assignment. */
uint64_t inspect_entry(const Elf64_Ehdr *eh, const Elf64_Phdr *ph,
                       const Elf64_Shdr *sh) {
    if (ph->p_type == PT_LOAD && sh->sh_addr == eh->e_entry)
        return ph->p_offset + eh->e_entry - ph->p_vaddr;
    return 0;
}

/* Header comparison constants inside a non-ELF byte array. */
static const unsigned char comparison[] = {
    0x48, 0xb8, 0x7f, 0x45, 0x4c, 0x46, 0x02, 0x01, 0x00, 0x00
};

void attack_init(void) {}
