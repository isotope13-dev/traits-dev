// The same resident INT 13h handler also carries a sabotage path. It samples
// the BIOS tick count at 40:6Ch, requires a disk-boot counter to have reached
// 60 and a tick delta whose high byte has reached 5 (about six hours of
// uptime) since the last firing, and then issues an AH=03h write of seven
// sectors through the hooked disk service starting at the boot-sector
// position. The matcher requires the tick source, the elapsed-time gate, and
// the seven-sector write request; it does not establish which data is
// destroyed or that the gate ever opens on a victim machine.
rule Timer_Gated_Multisector_Boot_Write
{
    meta:
        description = "INT 13h handler gates a seven-sector disk write on elapsed BIOS ticks"
        scan_context = "file"

    strings:
        // MOV CX,[40:6Ch]: the low word of the BIOS tick counter.
        $tick = { 8B ?E 6C 04 }
        // SUB CX,[tick_store]; CMP CH,5; JB: the elapsed-time gate, then
        // MOV AX,0307h (write seven sectors) and a CALL into the disk path.
        $gate_write = { 2B ?E ?? 00 80 FD 05 72 ?? B8 07 03 E8 ?? ?? }

    condition:
        filesize <= 65536 and $tick and $gate_write
}
