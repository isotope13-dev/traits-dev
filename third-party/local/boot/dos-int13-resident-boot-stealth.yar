// DOS resident boot-sector code in a raw sector. It reserves BIOS memory,
// routes the timer interrupt through relocated code that installs an INT 13h
// handler, then saves boot-sector data at sector 14, writes a body-spliced
// copy at sector 15, and redirects floppy boot-sector reads to the backup.
// The complete code path distinguishes this boot-sector implant from
// ordinary boot loaders and disk writers.
rule DOS_INT13_Resident_Boot_Stealth
{
    meta:
        description = "Resident INT 13h boot-sector stealth handler"
        scan_context = "file"

    strings:
        // BIOS memory-size word through BX, decrement, derive segment, copy
        // the loaded boot-sector body to the newly reserved top of memory.
        $resident_copy = { BB 13 04 [0-32] 8B 07 A3 0A 7C 48 89 07 B1 06 D3 E0 8E C0 B9 8D 01 F3 A4 }
        // Route INT 8h to the relocated code, whose guarded callback installs
        // that INT 13h vector.
        $timer_hook = { C7 06 20 00 CC 00 A3 22 00 }
        $timer_installs_int13 = { 2E A1 0A 00 A3 13 04 E8 ?? ?? C7 06 4C 00 00 01 8C 0E 4E 00 }
        // INT 13h handler restricts this branch to head 0, sector 1 reads.
        $boot_sector_handler = { 9C 55 50 53 51 52 56 57 1E 06 8B EC 83 F9 01 75 ?? 0A F6 75 ?? 3D 01 03 74 ?? 3D 01 02 75 ?? }
        // For floppy reads, rewrite the saved INT 13h request to head 1,
        // sector 14, where the clean boot-sector copy was saved.
        $floppy_read_redirect = { 80 FA 80 73 ?? 80 7E 0F 02 75 ?? 80 7F 18 0E 72 ?? C6 46 09 01 C6 46 0A 0E }
        // Save boot-sector data at sector 14, splice a jump and the resident
        // body into the buffer, then write that copy to sector 15.
        $backup_and_hidden_write = { B8 01 03 50 B1 0E [0-24] C7 07 EB 3C BE 3E 00 BF 3E 02 B9 4F 01 F3 A4 B6 00 41 58 9C FF 1E 06 00 }

    condition:
        filesize >= 512 and uint8(0) == 0xEB and uint16(510) == 0xAA55 and
        $resident_copy and @resident_copy[1] + !resident_copy[1] <= 512 and
        $timer_hook and @timer_hook[1] + !timer_hook[1] <= 512 and
        $timer_installs_int13 and @timer_installs_int13[1] + !timer_installs_int13[1] <= 512 and
        @timer_installs_int13[1] >= 0xCC and
        $boot_sector_handler and @boot_sector_handler[1] + !boot_sector_handler[1] <= 512 and
        $floppy_read_redirect and @floppy_read_redirect[1] + !floppy_read_redirect[1] <= 512 and
        @floppy_read_redirect[1] > @boot_sector_handler[1] and
        @floppy_read_redirect[1] < @boot_sector_handler[1] + 256 and
        $backup_and_hidden_write and @backup_and_hidden_write[1] + !backup_and_hidden_write[1] <= 512 and
        @backup_and_hidden_write[1] > @boot_sector_handler[1] and
        @backup_and_hidden_write[1] < @boot_sector_handler[1] + 256
}
