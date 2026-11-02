// A COM dropper or other carrier staging the read-intercept boot infector
// outside a 512-byte sector: the same five-leg cycle (sector-1/head-0
// request gate chaining through the saved INT 13h vector, one-sector
// backup write and clean re-read sharing that saved slot, fixed/floppy
// backup-sector select, and a write of the 7C00h-resident image back to
// sector 1) with all helper far calls proven to share one saved slot.
// Ordinary disk tools issue direct INT 13h requests; chaining a backup
// write and a clean re-read through one saved vector while rewriting
// sector 1 with a resident image only occurs in boot infectors.
rule Boot_Read_Intercept_Stealth_Carrier
{
    meta:
        description = "Carrier stages the resident INT 13h read-intercept boot infection cycle"
        scan_context = "file"

    strings:
        // CMP AH,02h; JNE; CMP CX,0001h; JNE; CMP DH,00h; JNE; PUSHF;
        // CALL FAR CS:[slot]: read gate on sector 1, head 0, chained on.
        $gate = { 80 FC 02 75 ?? 83 F9 01 75 ?? 80 FE 00 75 ?? 9C 2E FF 1E ?? ?? }
        // CMP AH,03h; JNE; CMP DL,80h; JB: fixed-disk writes routed in too.
        $wgate = { 80 FC 03 75 ?? 80 FA 80 72 ?? }
        // MOV AX,0301h; PUSHF; CALL FAR CS:[slot]: one-sector write, saved vector.
        $backup_write = { B8 01 03 9C 2E FF 1E ?? ?? }
        // MOV AX,0201h; PUSHF; CALL FAR CS:[slot]: one-sector re-read, saved vector.
        $stealth_read = { B8 01 02 9C 2E FF 1E ?? ?? }
        // MOV AX,0301h; MOV CX,0001h; MOV BX,7C00h; ...; PUSHF;
        // CALL FAR CS:[slot]: resident image written back to sector 1.
        $infect_write = { B8 01 03 B9 01 00 BB 00 7C [0-12] 9C 2E FF 1E ?? ?? }
        // MOV CL,sector; CMP DL,80h; JAE: fixed/floppy backup-sector select
        // shared by both helpers (sector 14 in the observed build).
        $chs = { B1 ?? 80 FA 80 73 ?? }

    condition:
        filesize > 512 and filesize <= 8192 and
        (#gate <= 8) and (#wgate <= 8) and
        (#gate > 0 or #wgate > 0) and
        (#backup_write > 0 and #backup_write <= 8) and
        (#stealth_read > 0 and #stealth_read <= 8) and
        (#infect_write > 0 and #infect_write <= 4) and
        (#chs > 0 and #chs <= 8) and
        for any c in (1..#chs) : (
            uint8(@chs[c] + 1) >= 2 and uint8(@chs[c] + 1) <= 63
        ) and
        for any w in (1..#backup_write) : (
            for any s in (1..#stealth_read) : (
                uint16(@backup_write[w] + 7) == uint16(@stealth_read[s] + 7) and
                (#gate == 0 or for any g in (1..#gate) : (
                    uint16(@gate[g] + 19) == uint16(@backup_write[w] + 7)
                ))
            )
        )
}
