// Boot code that reads the BIOS real-time-clock date (INT 1Ah AH=04h),
// branches on the BCD month/day in DX, then XOR-decodes an in-sector
// buffer and prints it through BIOS video (INT 10h) in a compare-gated
// loop. Calendar-gated code display with an obfuscated payload is the
// date-trigger half of a boot virus banner, not ordinary boot output.
rule Boot_RTC_Date_Gated_XOR_Video_Banner
{
    meta:
        description = "Boot code date-gates on the RTC, then XOR-decodes and displays a banner via BIOS video"
        scan_context = "file"

    strings:
        // MOV AH,04h; INT 1Ah; CMP DX,imm16; JB/JNE/JE/JA: date gate.
        $rtc = { B4 04 CD 1A 81 FA ?? ?? ( 72 ?? | 75 ?? | 74 ?? | 77 ?? ) }
        // MOV SI,imm16: banner buffer pointer loaded before the loop.
        $ptr = { BE ?? ?? }
        // LODSB; XOR AL,imm8 (nonzero); INT 10h: decode-and-display step.
        $xor = { AC 34 ?? CD 10 }
        // CMP AL,imm8; JNE with a negative displacement: the loop closes
        // backward over the decode step (forward skips are not loops).
        // Byte-class alternation keeps the direction proof in the string
        // so no value test on a deep iterator is needed.
        $term = { 3C ?? 75 ( 80|81|82|83|84|85|86|87|88|89|8A|8B|8C|8D|8E|8F|90|91|92|93|94|95|96|97|98|99|9A|9B|9C|9D|9E|9F|A0|A1|A2|A3|A4|A5|A6|A7|A8|A9|AA|AB|AC|AD|AE|AF|B0|B1|B2|B3|B4|B5|B6|B7|B8|B9|BA|BB|BC|BD|BE|BF|C0|C1|C2|C3|C4|C5|C6|C7|C8|C9|CA|CB|CC|CD|CE|CF|D0|D1|D2|D3|D4|D5|D6|D7|D8|D9|DA|DB|DC|DD|DE|DF|E0|E1|E2|E3|E4|E5|E6|E7|E8|E9|EA|EB|EC|ED|EE|EF|F0|F1|F2|F3|F4|F5|F6|F7|F8|F9|FA|FB|FC|FD|FE|FF ) }

    condition:
        filesize >= 512 and filesize <= 8192 and
        #rtc > 0 and #rtc <= 8 and
        #xor > 0 and #xor <= 8 and
        for any r in (1..#rtc) : (
            for any x in (1..#xor) : (
                @xor[x] > @rtc[r] and @xor[x] <= @rtc[r] + 96 and
                uint8(@xor[x] + 2) >= 1 and
                for any p in (1..#ptr) : (
                    @ptr[p] < @xor[x] and @ptr[p] + 32 >= @xor[x] and
                    for any t in (1..#term) : (
                        @term[t] > @xor[x] and @term[t] <= @xor[x] + 16
                    )
                )
            )
        )
}
