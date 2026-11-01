// Complete resident boot-sector / active-VBR infection cycle where the virus
// preserves a victim's BPB and boot tail by splicing them into its own
// resident 512-byte image at ES:0000h before writing ES:0000h back over the
// victim boot sector. Requires the 512-byte boot envelope, BIOS memory theft
// at 40:13h and 7C00h relocation, INT 13h vector capture and replacement
// storing the saved far pointer into the exact CS:[slot] invoked by the
// single-sector disk wrapper, self-marker verification comparing [0200h+off]
// against the sector's own marker byte at [off], dual REP MOVSB copies of
// victim BPB (0202h->0002h) and boot tail (03xxh->01xxh) into the resident
// image, setting BH=0 (ES:BX=ES:0000h), and calling the wrapper's AH=03h
// write entry.
rule Resident_Metadata_Splice_Boot_Infector
{
    meta:
        description = "Boot sector steals BIOS memory, hooks INT 13h, splices victim boot metadata into its resident body, and writes the sector back"
        scan_context = "file"

    strings:
        $mem_steal_a = { B1 06 [0-4] FF 0E 13 04 [0-4] A1 13 04 [0-2] D3 E0 }
        $mem_steal_b = { FF 0E 13 04 [0-4] A1 13 04 [0-2] B1 06 D3 E0 }
        $reloc = { BE 00 7C [0-6] ( B9 00 01 FC F3 A5 EA | B9 00 01 F3 A5 EA ) }
        // LES AX,[004Ch]; MOV word [004Ch],handler; MOV [004Eh],CS; PUSH CS; POP DS; MOV [slot],AX; MOV [slot+2],ES
        $vec_hook = { C4 06 4C 00 C7 06 4C 00 ?? ?? 8C 0E 4E 00 0E 1F A3 ?? ?? 8C 06 ?? ?? }
        // MOV AX,0301h; JMP +3; MOV AX,0201h; MOV DL,[drive]; PUSHF; CALL FAR CS:[slot]; RET
        $io_wrap = { B8 01 03 EB 03 B8 01 02 8A 16 ?? ?? 9C 2E FF 1E ?? ?? C3 }
        // CMP byte [02xxh],marker; JE ...; PUSH CX; MOV DI,0002h; MOV SI,0202h; MOV CX,len1; CLD; REP MOVSB;
        // MOV DI,01xxh; MOV SI,03xxh; MOV CX,len2; REP MOVSB; INC word [gen]; MOV BH,0; POP CX; CALL io_wrap
        $splice_write = { 80 3E ?? 02 ?? 74 ?? 51 BF 02 00 BE 02 02 B9 ?? 00 FC F3 A4 BF ?? 01 BE ?? 03 B9 ?? 00 F3 A4 FF 06 ?? 00 B7 00 59 E8 ?? ?? }

    condition:
        filesize == 512 and
        (uint8(0) == 0xEB or uint8(0) == 0xE9) and
        uint16(510) == 0xAA55 and
        ($mem_steal_a or $mem_steal_b) and
        $reloc and
        #vec_hook > 0 and #vec_hook <= 4 and
        #io_wrap > 0 and #io_wrap <= 4 and
        #splice_write > 0 and #splice_write <= 4 and
        for any h in (1..#vec_hook) : (
            uint16(@vec_hook[h] + 21) == uint16(@vec_hook[h] + 17) + 2 and
            for any w in (1..#io_wrap) : (
                uint16(@vec_hook[h] + 17) == uint16(@io_wrap[w] + 16) and
                for any s in (1..#splice_write) : (
                    uint16(@vec_hook[h] + 8) < @splice_write[s] and
                    uint8(@splice_write[s] + 4) == uint8(uint8(@splice_write[s] + 2)) and
                    uint8(@splice_write[s] + 15) >= 0x24 and
                    uint8(@splice_write[s] + 21) == uint8(@splice_write[s] + 24) and
                    @splice_write[s] + 41 + int16(@splice_write[s] + 39) == @io_wrap[w]
                )
            )
        )
}
