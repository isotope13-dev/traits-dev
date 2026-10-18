#!/usr/bin/env python3
"""Generate seed-independent encoded-reference matchers; no specimen keys/addresses."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
# The scalar equivalent of the observed 64-bit index-derived xorshift codec.
# Only the low 15 state bits affect a decoded byte:
# k(i) = (s ^ (s >> 7) ^ (s << 6)) & 255, s = seed + i*0x7c15.
KEY = "B8 B9 79 37 9E F7 E? 8B ?? B8 15 7C 4A 7F F7 E? 03 ?? 8B ?? 81 ( C6 | C7 ) [4] 8B ?? 81 ( D3 | D7 ) [4] 8B ?? 0F A4 ?? 0D C1 ?? 0D"
FORMS = [
    ("ebp8", "C7 45 ?? [4] C7 45 ?? [4] C7 45 ?? ?? ?? ?? ??", 3, 7),
    ("ebp32", "C7 85 [8] C7 85 [8] C7 85 ?? ?? ?? ?? ?? ?? ?? ??", 6, 10),
    ("esp8", "C7 44 24 ?? [4] C7 44 24 ?? [4] C7 44 24 ?? ?? ?? ?? ??", 4, 8),
    ("ebp8-cross", "", 0, 0),
]
TARGETS = [
    ("micro-behaviors/communications/http/client/winhttp", "x86-xorshift-send-request-prefix", "Keystream encoded WinHttpSendRequest name prefix", b"WinHttpSendReque"),
    ("micro-behaviors/os/security/dpapi", "x86-xorshift-dpapi-prefix", "Keystream encoded CryptUnprotectData name prefix", b"CryptUnprotectDa"),
    ("micro-behaviors/communications/http/services/telegram", "x86-xorshift-api-host", "Keystream encoded Telegram API hostname", b"api.telegram.org"),
    ("micro-behaviors/communications/http/services/telegram", "x86-xorshift-document-method-prefix", "Encoded Telegram sendDocument path prefix", b"/sendDocumen"),
    ("micro-behaviors/data/db/access", "x86-xorshift-login-columns-prefix", "Keystream encoded browser credential SQL prefix", b"SELECT origin_url, username_value, password_valu"),
    ("micro-behaviors/os/registry/keys/autostart", "x86-xorshift-run-key-prefix", "Keystream encoded CurrentVersion Run key prefix", b"Software\\Microsoft\\Windows\\CurrentVersion\\Ru"),
]

def matcher(identifier, wanted):
    # Match counts are capped by the host scanner. Boolean anchors are safe;
    # locate the witness using bounded byte reads, not @pattern[n] arrays.
    # The relative call must target the decoder containing this seed, and its
    # LEA source must name the first ciphertext store's stack slot.
    assert len(wanted) % 4 == 0 and len(wanted) >= 12
    lines = ['import "pe"', f"rule {identifier.replace('-', '_')} {{", "  strings:",
             "    $call_ebp8 = { 68 [4] 8D 4D ?? E8 ?? ?? ?? ?? }",
             "    $call_ebp32 = { 68 [4] 8D 8D [4] E8 ?? ?? ?? ?? }",
             "    $call_esp8 = { 68 [4] 8D 4C 24 ?? E8 ?? ?? ?? ?? }",
             "  condition:",
             "    pe.is_pe and filesize < 16MB and any of ($call_*) and",
             "    for any section in (0..pe.number_of_sections-1) : (",
             "      pe.sections[section].characteristics & pe.SECTION_MEM_EXECUTE != 0 and",
             "      pe.sections[section].raw_data_size >= 16 and",
             "    for any c in (pe.sections[section].raw_data_offset+11..pe.sections[section].raw_data_offset+pe.sections[section].raw_data_size-5) : (",
             "      uint8(c) == 0xe8 and",
             "      ((uint8(c-8) == 0x68 and uint16(c-3) == 0x4d8d) or",
             "       (uint8(c-11) == 0x68 and uint16(c-6) == 0x8d8d) or",
             "       (uint8(c-9) == 0x68 and uint16(c-4) == 0x4c8d and uint8(c-2) == 0x24)) and",
             "      with target = c+5+int32(c+1) : (",
             "        target >= pe.sections[section].raw_data_offset and target+768 < filesize and",
             "        for any k in (target..target+768) : (",
             "          k+43 <= pe.sections[section].raw_data_offset+pe.sections[section].raw_data_size and",
             "          uint32(k) == 0x3779b9b8 and uint8(k+4) == 0x9e and",
             "          uint8(k+9) == 0xb8 and uint32(k+10) == 0x7f4a7c15 and",
             "          (uint16(k+20) == 0xc781 or uint16(k+20) == 0xc681) and",
             "          uint8(k+28) == 0x81 and (uint8(k+29) == 0xd3 or uint8(k+29) == 0xd7) and",
             "          uint16(k+36) == 0xa40f and uint8(k+39) == 13 and uint8(k+42) == 13 and",
             "          with seed = uint16(k+22) : (",
             "            for any base in (c-768..c-12) : (",
             "              base >= pe.sections[section].raw_data_offset and ("]
    for form_index, (name, _, displacement, stride) in enumerate(FORMS):
        if name == 'ebp8':
            gate = "uint8(c-8) == 0x68 and uint16(c-3) == 0x4d8d and uint16(base) == 0x45c7 and uint8(base+2) == uint8(c-1)"
        elif name == 'ebp32':
            gate = "uint8(c-11) == 0x68 and uint16(c-6) == 0x8d8d and uint16(base) == 0x85c7 and int32(base+2) == int32(c-4)"
        elif name == 'esp8':
            gate = "uint8(c-9) == 0x68 and uint16(c-4) == 0x4c8d and uint8(c-2) == 0x24 and uint16(base) == 0x44c7 and uint8(base+2) == 0x24 and uint8(base+3)+4 == uint8(c-1)"
        else:
            gate = "uint8(c-8) == 0x68 and uint16(c-3) == 0x4d8d and uint16(base) == 0x45c7 and uint8(base+2) == uint8(c-1) and uint8(base+2) < 128"
        lines += ["                " + ("or " if form_index else "") + "(", "                  " + gate + " and"]
        for start in range(0, len(wanted), 8):
            chunk = wanted[start:start + 8]
            end = start + len(chunk) - 1
            literal = int.from_bytes(chunk, "little")
            lines += ["                  " + ("and " if start else "") + f"for all j in ({start}..{end}) : (", "                    with state = seed + j*0x7c15 : ("]
            mask = "((state ^ (state >> 7) ^ (state << 6)) & 255)"
            expected = f"((0x{literal:x} >> ((j-{start})*8)) & 255)"
            if name == "ebp8-cross":
                lines += ["                      with short = (131-uint8(base+2))\\4 : (", f"                        ((j\\4) < short and (uint8(base+3+(j\\4)*7+j%4) ^ {mask}) == {expected}) or", f"                        ((j\\4) >= short and (uint8(base+6+(j\\4)*10-short*3+j%4) ^ {mask}) == {expected})", "                      )"]
            else:
                lines += [f"                      (uint8(base + {displacement} + (j\\4)*{stride} + j%4) ^", f"                       {mask}) == {expected}"]
            lines += ["                    )", "                  )"]
        lines += ["                )"]
    lines += ["              )", "            )", "          )", "        )", "      )", "    )", "    )", "}"]
    return "\n".join(lines)


def main():
    grouped = {}
    for directory, identifier, description, wanted in TARGETS:
        grouped.setdefault(directory, []).append((identifier, description, matcher(identifier, wanted)))
    for directory, entries in grouped.items():
        lines = ["# Generated by testdata/triage/native-xorshift-stealer/generate.py.", "# Recover encoded references using the codec's own variable seed, without", "# requiring a campaign key, address, destination, filename, or plaintext copy.", "# Follow the relative decoder call and its stack-source LEA; match the seed", "# inside that decoder. No network or credential-transfer claim is made.", "defaults:", "  platforms: [windows]", "  for: [pe, dll]", "  arch: [x86]", "  crit: notable", "  conf: 0.98", "", "traits:"]
        for identifier, description, source in entries:
            lines += [f"  - id: {identifier}", f"    desc: {description}", "    if:", "      type: yara", "      source: |"]
            lines += ["        " + line for line in source.splitlines()]
        output = ROOT / directory / "xorshift-stack.yaml"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
