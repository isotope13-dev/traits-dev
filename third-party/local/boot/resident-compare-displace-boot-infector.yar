// Resident boot-sector infector of the Aircop shape: the whole infection
// cycle fits in the 512-byte boot record. It reserves the top kilobyte of
// conventional memory (DEC word [40:13h], INT 12h, shift into a segment),
// saves both INT 19h vector words with XCHG, copies all 256 words from
// 0000:7C00h into the reserved segment, installs its resident handlers with
// an indexed two-word IVT swap loop (INT 12h at 0:48h, INT 13h at 0:4Ch),
// and filters floppy INT 13h traffic through a read-compare-infect core:
// read the addressed sector into a scratch buffer, REPE CMPSB against the
// resident body, and when it differs overwrite the boot position while
// displacing the victim sector to a backup cylinder with a second write.
// Legitimate boot code relocates itself and loads the next stage, and drive
// overlays may steal memory and hook INT 13h, but neither saves INT 19h with
// XCHG, swaps the IVT through this loop, nor rewrites an intercepted sector
// with its own body while displacing the original elsewhere.
rule Resident_Compare_Displace_Boot_Infector
{
    meta:
        description = "Boot sector steals BIOS memory, saves INT 19h, swaps IVT handlers, and displaces boot sectors after compare"
        scan_context = "file"

    strings:
        // DEC word [0413h]; INT 12h; MOV CL,6; SHL AX,CL: shrink the BIOS
        // memory-size word and turn the new top of memory into a segment.
        $mem_steal = { FF 0E 13 04 [0-6] CD 12 [0-8] B1 06 D3 E0 }
        // XCHG [0066h],AX ... MOV AX,imm; XCHG [0064h],AX: save both words
        // of the INT 19h bootstrap vector into resident slots.
        $int19_save = { 87 06 66 00 [0-16] B8 ?? ?? 87 06 64 00 }
        // MOV BX/SI,7C00h; ... MOV CX,0100h; [CLD;] REP MOVSW: relocate the
        // whole 512-byte sector into the reserved top-of-memory segment.
        $reloc = { ( BB 00 7C | BE 00 7C ) [0-8] B9 00 01 [0-8] ( FC F3 A5 | F3 A5 ) }
        // MOV BX,0048h/004Ch; ... MOV CL,2; MOV AX,[BX]; XCHG CS:[BX+SI],AX;
        // MOV [BX],AX; INC BX; INC BX; LOOP: exchange two IVT words with the
        // resident handler slots.
        $swap_loop = { BB ( 48 00 | 4C 00 ) [0-24] B1 02 8B 07 2E 87 00 89 07 43 43 E2 F5 }
        // PUSH CS; POP ES; MOV AH,2; CALL read; JNC; PUSH ES; POP DS;
        // MOV SI,body; MOV DI,buffer+body; MOV CX,len; PUSH SI; PUSH DI; CLD;
        // REPE CMPSB; POP SI; POP DI; JE chain; DEC SI; DEC DI; MOV CX,len2;
        // STD; REP MOVSB; XOR BX,BX; MOV AH,3; CALL write: the
        // read-compare-copy-write infection core.
        $infect_core = { 0E 07 B4 02 E8 ?? ?? 72 ?? 06 1F BE ?? ?? BF ?? ?? B9 ?? ?? 56 57 FC F3 A6 5E 5F 74 ?? 4E 4F B9 ?? ?? FD F3 A4 33 DB B4 03 E8 ?? ?? }
        // MOV BX,0200h; MOV AH,3; CALL write: the second write displaces the
        // victim sector into the backup position.
        $displace_write = { BB 00 02 B4 03 E8 ?? ?? }

    condition:
        filesize == 512 and
        (uint8(0) == 0xEB or uint8(0) == 0xE9) and
        uint16(510) == 0xAA55 and
        $mem_steal and $int19_save and $reloc and $swap_loop and
        $infect_core and $displace_write and
        for any c in (1..#infect_core) : (
            for any d in (1..#displace_write) : (
                @displace_write[d] > @infect_core[c]
            )
        )
}
