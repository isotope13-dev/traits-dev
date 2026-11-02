// A boot record that filters disk requests and forwards selected requests
// through the previous INT 13h vector. Disk overlays can use this design,
// so it is a suspicious capability rather than an infection claim.
rule DDO_INT13_Sector_Filter
{
    meta:
        description = "Boot record conditionally forwards disk requests through an INT 13h filter"
        scan_context = "file"

    strings:
        // Compare drive and sector bounds, then far-call the prior BIOS vector.
        $sector_filter = { 80 FA 80 72 ?? 80 FE 02 77 ?? 02 E5 80 C1 04 9C 2E FF 1E 60 00 9D CA 02 00 }

    condition:
        filesize == 512 and
        (uint8(0) == 0xEB or uint8(0) == 0xE9) and
        uint16(510) == 0xAA55 and
        $sector_filter
}
