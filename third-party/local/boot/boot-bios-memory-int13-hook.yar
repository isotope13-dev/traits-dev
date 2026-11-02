// A boot sector that reserves a kilobyte at the top of conventional memory
// by decrementing the BIOS memory-size word at 40:13h, shifts the new top of
// memory into a segment, copies all 256 words of 0000:7C00h into that segment
// before far-jumping there (or rebooting through INT 19h so the relocated
// copy takes over), and captures and replaces the INT 13h vector at
// 0000:004Ch/004Eh. Dynamic drive overlays can also reserve BIOS memory and
// hook INT 13h without infecting sectors, so this residency-and-hook fragment
// is overridden to suspicious while the complete infection cycle is hostile.
// Register allocation varies: the steal may shift BX rather than AX, the
// relocation may stage 7C00h through AX instead of SI, and the vector capture
// may use CX loads with the steal block sitting between capture and replace.
rule Boot_BIOS_Memory_Steal_INT13_Hook
{
    meta:
        description = "Boot sector steals BIOS memory, relocates from 7C00h, and hooks INT 13h"
        scan_context = "file"

    strings:
        // MOV CL,6; ... DEC word [0413h]; MOV AX,[0413h]; SHL AX,CL
        $mem_steal_a = { B1 06 [0-4] FF 0E 13 04 [0-4] A1 13 04 [0-2] D3 E0 }
        // DEC word [0413h]; MOV AX,[0413h]; MOV CL,6; SHL AX,CL
        $mem_steal_b = { FF 0E 13 04 [0-4] A1 13 04 [0-2] B1 06 D3 E0 }
        // BX=0413h; DEC word [BX]; MOV AX,[BX]; MOV CL,6; SHL AX,CL
        // (register-indirect form of the same 40:13h shrink)
        $mem_steal_bx = { ( B7 04 B3 13 | B3 13 B7 04 ) [0-8] ( FF 0F 8B 07 | 8B 07 FF 0F ) [0-4] B1 06 D3 E0 }
        // MOV BX,[0413h]; DEC BX; MOV [0413h],BX; MOV CL,6; SHL BX,CL
        // (direct-address form shifting the stolen size in BX)
        $mem_steal_bx_direct = { 8B 1E 13 04 4B 89 1E 13 04 [0-4] ( B1 06 | B9 06 ?? ) D3 E3 }
        // MOV SI,7C00h; ... MOV CX,0100h; [CLD;] REP MOVSW; JMP FAR or INT 19h
        // (reboot installs the relocated copy instead of far-jumping to it)
        $reloc = { BE 00 7C [0-6] ( B9 00 01 FC F3 A5 EA | B9 00 01 F3 A5 EA | B9 00 01 FC F3 A5 CD 19 | B9 00 01 F3 A5 CD 19 ) }
        // MOV AX,7C00h; ... MOV CX,0100h; [CLD;] REP MOVSW; JMP FAR or INT 19h
        // (7C00h staged through AX with hook/steal code between stage and copy)
        $reloc_ax = { B8 00 7C [0-64] B9 00 01 [0-4] ( FC F3 A5 EA | F3 A5 EA | FC F3 A5 CD 19 | F3 A5 CD 19 ) }
        // LES AX,[004Ch]; MOV word [004Ch],imm16; MOV [004Eh],CS
        $vec_hook_les = { C4 06 4C 00 C7 06 4C 00 ?? ?? 8C 0E 4E 00 }
        // MOV AX,[004Ch]; ... MOV reg,[004Eh]; ... MOV word [004Ch],imm16; MOV [004Eh],seg
        $vec_hook_mov = { A1 4C 00 [0-8] 8B ?? 4E 00 [0-12] C7 06 4C 00 ?? ?? ( 8C 0E 4E 00 | 89 ?? 4E 00 | A3 4E 00 ) }
        // MOV reg,[004Ch]; ... MOV reg,[004Eh]; ... MOV word [004Ch],imm16;
        // MOV [004Eh],seg (the two halves may sit apart when the steal block
        // runs between capture and replace)
        $vec_hook_mov_wide = { ( A1 4C 00 | 8B ?? 4C 00 ) [0-8] ( A1 4E 00 | 8B ?? 4E 00 ) [0-64] C7 06 4C 00 ?? ?? ( 8C 0E 4E 00 | 89 ?? 4E 00 | A3 4E 00 ) }
        // BX=004Ch; LES AX,[BX] (save INT 13h); BX=004Eh; MOV [BX],AX (segment);
        // BX=004Ch; MOV AX,imm; MOV [BX],AX (offset): BX-indirect vector swap
        $vec_hook_bx = { BB 4C 00 C4 07 [0-32] BB 4E 00 89 07 [0-12] BB 4C 00 B8 ?? ?? 89 07 }

    condition:
        filesize == 512 and
        (uint8(0) == 0xEB or uint8(0) == 0xE9) and
        uint16(510) == 0xAA55 and
        ($mem_steal_a or $mem_steal_b or $mem_steal_bx or $mem_steal_bx_direct) and
        ($reloc or $reloc_ax) and
        ($vec_hook_les or $vec_hook_mov or $vec_hook_mov_wide or $vec_hook_bx)
}
