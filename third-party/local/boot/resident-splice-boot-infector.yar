// A resident boot-sector virus of the Stoned shape carries its whole
// infection cycle in the 512-byte boot record it leaves on every disk it
// touches. This rule requires the cycle, not a family byte: the boot envelope
// (a 512-byte sector with a JMP at offset 0 and the 55AAh signature at 510),
// residency by shrinking the BIOS memory-size word at 40:13h and converting
// the stolen top of memory into a segment, theft of the INT 13h vector at
// 0:4Ch/0:4Eh, a resident read filter that picks out single-sector boot reads
// (AH=02h, head 0, sector 1) and chains them to the saved vector, dual
// splices that copy the victim BPB and the partition table from a sector
// buffer into the resident image with REP MOVSW, and an AH=03h write of that
// image back over the boot sector through BIOS. Legitimate boot code
// relocates itself and loads the next stage; it never shrinks the BIOS memory
// map, filters disk reads in a resident handler, nor plants victim metadata
// into its own body before rewriting the boot sector.
rule Resident_Splice_Boot_Infector
{
    meta:
        description = "Resident boot code hooks INT 13h, splices victim boot metadata into its image, and writes the boot sector back"
        scan_context = "file"

    strings:
        // MOV CL,6; ... DEC word [40:13h]; MOV AX,[40:13h]; SHL AX,CL
        $steal_ax_a = { B1 06 [0-4] FF 0E 13 04 [0-4] A1 13 04 [0-2] D3 E0 }
        // DEC word [40:13h]; MOV AX,[40:13h]; MOV CL,6; SHL AX,CL
        $steal_ax_b = { FF 0E 13 04 [0-4] A1 13 04 [0-2] B1 06 D3 E0 }
        // MOV BX,[40:13h]; DEC BX; MOV [40:13h],BX; MOV CX,imm; SHL BX,CL
        $steal_bx = { 8B 1E 13 04 4B 89 1E 13 04 [0-4] ( B1 06 | B9 06 ?? ) D3 E3 }
        // LES AX,[004Ch]; MOV word [004Ch],imm16; MOV [004Eh],CS
        $hook_les = { C4 06 4C 00 C7 06 4C 00 ?? ?? 8C 0E 4E 00 }
        // LES AX,[004Ch]; ... MOV word [004Ch],imm; MOV [004Eh],CS: the same
        // LES capture/replace with the saved-vector stores between the halves.
        $hook_les_wide = { C4 06 4C 00 [0-16] C7 06 4C 00 ?? ?? 8C 0E 4E 00 }
        // MOV AX,[004Ch]; ... MOV reg,[004Eh]; ... MOV word [004Ch],imm16;
        // MOV [004Eh],seg (the two halves may sit apart when the steal block
        // runs between capture and replace).
        $hook_mov = { ( A1 4C 00 | 8B ?? 4C 00 ) [0-8] ( A1 4E 00 | 8B ?? 4E 00 ) [0-64] C7 06 4C 00 ?? ?? ( 8C 0E 4E 00 | 89 ?? 4E 00 | A3 4E 00 ) }
        // CMP AH,02h; ... CMP DH,00h; ... CMP CX,0001h; PUSHF; CALL FAR
        // CS:[slot]: the resident filter admits single-sector boot reads
        // before chaining them to the saved disk vector.
        $boot_read_gate = { 80 FC 02 75 ?? 80 FE 00 75 ?? 83 F9 01 75 ?? 9C 2E FF 1E ?? ?? }
        // MOV SI,020Bh; MOV CX,len; ... REP MOVSW: copy the victim BPB from
        // the sector buffer into the resident image past its jump.
        $bpb_splice = { BE 0B 02 B9 ?? ?? [0-4] F3 A5 }
        // MOV SI,xx03h; MOV CL,len; MOV DI,01BEh; REP MOVSW: copy the victim
        // partition table from the sector buffer into the resident image.
        $part_splice = { BE ?? 03 B1 ?? BF BE 01 F3 A5 }
        // MOV AX,0301h; ... PUSHF; CALL FAR [slot]: write the spliced image
        // back through the saved disk vector.
        $boot_write = { B8 01 03 [0-12] 9C ( 2E FF 1E | FF 1E ) ?? ?? }

    condition:
        filesize == 512 and
        (uint8(0) == 0xEB or uint8(0) == 0xE9) and
        uint16(510) == 0xAA55 and
        ($steal_ax_a or $steal_ax_b or $steal_bx) and
        ($hook_les or $hook_les_wide or $hook_mov) and
        $boot_read_gate and
        $bpb_splice and
        $part_splice and
        $boot_write
}
