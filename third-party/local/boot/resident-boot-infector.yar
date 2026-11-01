// A boot-sector virus of the ABS3 shape carries its whole infection cycle in
// the 512-byte boot record it leaves on every disk it touches. This rule
// requires the cycle, not a family byte: the boot envelope (a 512-byte sector
// with a JMP at offset 0 and the 55AAh signature at 510), residency by
// shrinking the BIOS memory-size word at 40:13h and converting the stolen top
// of memory into a segment, theft of the INT 13h vector at 0:4Ch/0:4Eh, and
// the splice that plants a JMP stub at offset 0 of a sector buffer, copies the
// body over the original code past the BPB, and writes the sector back with
// AH=03h. Legitimate boot code relocates itself and loads the next stage; it
// never shrinks the BIOS memory map nor rewrites sectors it reads into its
// own body.
rule Resident_Boot_Sector_Infector
{
    meta:
        description = "Boot sector steals BIOS memory, hooks INT 13h, and rewrites boot sectors with its body"
        scan_context = "file"

    strings:
        // DEC word [40:13h]; MOV AX,[40:13h]; MOV CL,6; SHL AX,CL: reserve
        // the top kilobyte of BIOS memory and turn it into a segment.
        $mem_steal = { FF 0E 13 04 [0-4] A1 13 04 [0-2] B1 06 D3 E0 }
        // MOV BX,[0:4Eh]; MOV [0:4Eh],AX; MOV AX,[0:4Ch]; MOV word [0:4Ch],imm:
        // save the INT 13h vector and repoint it at the resident handler.
        $vec_swap = { 8B 1E 4E 00 A3 4E 00 A1 4C 00 [0-8] C7 06 4C 00 }
        // MOV word [BX],EBxxh: plant a short JMP stub at offset 0 of the
        // sector buffer just read.
        $jmp_patch = { C7 07 EB ?? }
        // MOV CX,0x1xx; REP MOVSB (copy the body past the BPB), then MOV AH,3:
        // write the spliced sector back through BIOS.
        $body_write = { B9 ?? 01 F3 A4 [0-24] B4 03 }

    condition:
        filesize == 512 and uint8(0) == 0xEB and uint16(510) == 0xAA55 and
        all of them
}
