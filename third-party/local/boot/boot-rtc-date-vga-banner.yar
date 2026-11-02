// A 512-byte boot record that queries the BIOS calendar (INT 1Ah AH=04h),
// compares the month/day pair against a trigger, and on a match renders a
// banner straight into VGA color RAM at segment B800h with a decoded-byte
// loop. Ordinary loaders and managers never gate screen output on the
// calendar; boot viruses use the trigger to time defacement. The envelope
// keeps this to boot-shaped records so calendar checks in larger programs
// stay out of scope.
rule Boot_RTC_Date_VGA_Banner
{
    meta:
        description = "Boot record renders calendar-gated banner into VGA RAM"
        scan_context = "file"

    strings:
        // MOV AH,04h; INT 1Ah; CMP DX,imm16: read the BIOS calendar and
        // compare month/day against the trigger value.
        $date_gate = { B4 04 CD 1A 81 FA ?? ?? }
        // MOV AX,B800h; MOV ES,AX: point ES at VGA color RAM.
        $vga_seg = { B8 00 B8 8E C0 }
        // LODSB; CMP AL,00h; JA +n; ADD DI,4Ch: fetch banner bytes and step
        // a row on the terminator while decoding the banner stream.
        $banner_decode = { AC 3C 00 77 ?? 83 C7 4C }

    condition:
        filesize == 512 and
        (uint8(0) == 0xEB or uint8(0) == 0xE9) and
        uint16(510) == 0xAA55 and
        $date_gate and $vga_seg and $banner_decode
}
