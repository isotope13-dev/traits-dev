// Boot-sector payload banner of the Aircop shape: a NUL-terminated string
// printer that skips plain ASCII bytes via JNS, decodes sign-bit-set bytes
// with a nonzero single-byte XOR key, sets a blinking video attribute
// (BL |= 88h), paces output with a LOOP delay, and emits each character
// twice through INT 10h (AH=09h write with attribute, AH=0Eh teletype).
// Legitimate boot messages print plain text; the JNS-gated XOR decode loop
// with a blinking attribute exists to hide the payload text at rest.
rule Boot_XOR_Blinking_Teletype_Banner
{
    meta:
        description = "Boot code prints an XOR-decoded blinking INT 10h banner"
        scan_context = "file"

    strings:
        // MOV BX,7; CLD; LODSB; OR AL,AL; JZ end; JNS skip; XOR AL,key;
        // OR BL,88h; [INT 9]; CMP AL,20h; JBE teletype; MOV CH,40h; LOOP $;
        // INC CX; MOV AH,9; INT 10h; MOV AH,0Eh; INT 10h: the decoder.
        $decoder = { BB 07 00 FC AC 0A C0 74 ?? 79 ?? 34 ?? 80 CB 88 ( CD 09 3C 20 | 3C 20 ) 76 ?? B5 ?? E2 FE 41 B4 09 CD 10 B4 0E CD 10 }

    condition:
        filesize <= 8192 and
        #decoder > 0 and #decoder <= 8 and
        for any d in (1..#decoder) : (
            uint8(@decoder[d] + 12) != 0
        )
}
