// From inside a hooked INT 13h handler: filter for read requests (AH=02h),
// sample the BIOS clock via INT 1Ah (AH=00h) and skip unless an elapsed-tick
// threshold has passed since the last probe, read CHS 0/0/1 into a scratch
// buffer at offset 0200h through a saved INT 13h far vector, and when DL has
// the fixed-disk bit (80h) set, walk the four 16-byte MBR partition entries
// at 03BEh (0200h + 01BEh) for the active flag (80h) and read that active
// partition's volume boot record into 0200h through the same saved vector.
rule INT13_Tick_Gated_Partition_VBR_Probe
{
    meta:
        description = "INT 13h read filter throttles on BIOS ticks and reads active partition VBR"
        scan_context = "file"

    strings:
        // MOV AX,0201h; MOV DL,[drive]; PUSHF; CALL FAR CS:[saved_int13]; RET
        $io_read = { B8 01 02 8A 16 ?? ?? 9C 2E FF 1E ?? ?? C3 }
        // CMP AH,02h; JNE ...; XOR AH,AH / MOV AH,0; INT 1Ah; ... SUB DX,[last]; ... SUB DX,imm8; JL/JB
        $tick_gate = { 80 FC 02 75 ?? [0-8] ( 32 E4 CD 1A | B4 00 CD 1A ) [0-4] 2B 16 ?? ?? [0-6] 83 EA ?? ( 7C ?? | 72 ?? ) }
        // MOV BX,0200h; CALL io_read; JC ...; TEST DL,80h; JZ ...; MOV CL,4; MOV DI,03BEh;
        // CMP byte [DI],80h; JE +5; ADD DI,10h; LOOP; MOV DH,[DI+1]; MOV CX,[DI+2]; CALL io_read
        $vbr_probe = { BB 00 02 E8 ?? ?? 72 ?? F6 C2 80 74 ?? B1 04 BF BE 03 80 3D 80 74 05 83 C7 10 E2 F6 8A 75 01 8B 4D 02 E8 ?? ?? }

    condition:
        filesize >= 512 and filesize <= 8192 and
        #io_read > 0 and #io_read <= 8 and
        #tick_gate > 0 and #tick_gate <= 8 and
        #vbr_probe > 0 and #vbr_probe <= 8 and
        for any g in (1..#tick_gate) : (
            for any p in (1..#vbr_probe) : (
                @vbr_probe[p] > @tick_gate[g] and @vbr_probe[p] <= @tick_gate[g] + 64 and
                for any r in (1..#io_read) : (
                    @vbr_probe[p] + 6 + int16(@vbr_probe[p] + 4) == @io_read[r] and
                    @vbr_probe[p] + 37 + int16(@vbr_probe[p] + 35) == @io_read[r]
                )
            )
        )
}
