// From inside the resident INT 13h handler an infected boot sector installs:
// every request aimed at head 0, sector 1 -- the boot-sector position --
// for read (AH=02h) or write (AH=03h) is retargeted at the sector holding
// the saved original before the request continues. Reads of the infected
// boot sector return the clean backup, and attempts to overwrite the virus's
// sector are diverted away from it. No legitimate boot manager or disk
// filter rewrites a caller's CHS address this way.
rule Boot_Sector_Backup_Redirect
{
    meta:
        description = "Resident INT 13h hook redirects boot-sector reads and writes to a backup sector"
        scan_context = "file"

    strings:
        // PUSHF; PUSH DS; register saves: the interrupt-handler prologue
        // that leads into the request filter.
        $hook_entry = { 9C 1E [0-16] 80 FE 00 }
        // CMP DH,0; JNZ; CMP CX,1; JNZ (head 0, sector 1); CMP AH,3; JZ;
        // CMP AH,2; JNZ (write or read); POP AX; POP CX; POP DX; MOV CX,imm:
        // retarget the request at the backup sector before chaining on.
        $redirect = { 80 FE 00 75 ?? 83 F9 01 75 ?? 80 FC 03 74 ?? 80 FC 02 75 ?? 58 59 5A B9 ?? 00 }

    condition:
        filesize <= 65536 and $hook_entry and $redirect
}
