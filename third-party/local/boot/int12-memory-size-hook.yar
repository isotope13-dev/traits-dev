// Boot code that repoints the BIOS memory-size vector (INT 12h at
// 0000:0048h/004Ah) at its own handler, where the handler reads the
// BIOS conventional-memory-size word at 40:13h and reports the unshrunk
// size (or returns 639) so the kilobyte stolen for residency stays
// hidden from later size checks. Installing a memory-size handler is
// not something boot managers or overlays do; they leave INT 12h alone.
rule Boot_INT12_Memory_Size_Hook
{
    meta:
        description = "Boot code repoints INT 12h at a handler that lies about BIOS conventional memory size"
        scan_context = "file"

    strings:
        // BX=004Ah; MOV [BX],AX: INT 12h segment replaced.
        $seg = { BB 4A 00 89 07 }
        // BX=0048h; MOV AX,imm; MOV [BX],AX: INT 12h offset replaced.
        $off = { BB 48 00 B8 ?? ?? 89 07 }
        // BX=0413h ... MOV ES:[BX],AX: handler restores the full size word.
        $size_read = { B7 04 B3 13 [0-32] 26 89 07 }
        // MOV AX,027Fh: handler returns 639 (one hidden kilobyte).
        $size_lie = { B8 7F 02 }

    condition:
        filesize >= 512 and filesize <= 8192 and
        #seg > 0 and #seg <= 8 and
        #off > 0 and #off <= 8 and
        for any s in (1..#seg) : (
            for any o in (1..#off) : (
                @off[o] >= @seg[s] and @off[o] <= @seg[s] + 32 and
                (
                    (#size_read > 0 and for any r in (1..#size_read) : (
                        @size_read[r] > @off[o] and @size_read[r] <= @off[o] + 512
                    )) or
                    (#size_lie > 0 and for any l in (1..#size_lie) : (
                        @size_lie[l] > @off[o] and @size_lie[l] <= @off[o] + 512
                    ))
                )
            )
        )
}
