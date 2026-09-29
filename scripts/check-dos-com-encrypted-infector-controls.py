#!/usr/bin/env python3
"""Check DOS word-XOR infectors and nonmatching controls."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = {
    "champaigne-523": "c87a27c33534e935fb0e4047eb30e1a60dddddf17f2c14c910cbd3bb1939a367",
    "champaigne-636": "7deebbe4b6dd4ba702a7215b72faf3fac5aa55061322c6dfda68bff961e93931",
    "champaigne-691": "abb875e75fb775842202ef6a663f718a684a60aa6bab501e2418f2389f2225fa",
}
WORD_XOR = "objectives/anti-static/obfuscation/payload/polymorphic::dos-fixed-key-xor-word-si-loop"
ENCRYPTED = "objectives/anti-static/obfuscation/payload/polymorphic::dos-encrypted-virus-body"
INFECTOR = "objectives/impact/infect/binary/dos/com-bytes/file::dos-parasitic-encrypted-infector"
NOSTARDAMUS_INFECTOR = "objectives/impact/infect/binary/dos/com-bytes/interrupt::dos-int21-search-hook-hides-appended-body"
NOSTARDAMUS_HIDDEN_APPEND = "objectives/impact/infect/binary/dos/com-bytes/interrupt::dos-com-hidden-body-appender"
NOSTARDAMUS_SEARCH_HOOK = "objectives/impact/infect/binary/dos/com-bytes/interrupt::dos-int21-stealth-directory-search"
NOSTARDAMUS_SHA256 = "5298db2f904e81c7ecb0a78c03ea8917f65405c03bd0a6451fe002a5fd24353e"
FULLDEAD_DISK_INFECTOR = "objectives/impact/wipe/disk/mbr::dos-com-infector-with-lowmem-disk-write"
FULLDEAD_DISK_GATE = "objectives/impact/wipe/disk/mbr::dos-int13-dead-counter-gate"
FULLDEAD_FILE_INFECTOR = "objectives/impact/infect/binary/dos/com-bytes/file::dos-com-directory-infector"
FULLDEAD_SHA256 = "379d014569ad275035bfe9ccaaa7a54417685e70a0123bd71e242073dac6a951"
TCHECHEN_SHA256 = "64634c2eb835129974f1d803fe9f4ecc8b029a86b39841b2240956f53f91a392"
TCHECHEN_BOOT_ENGINE = "objectives/impact/infect/boot-sector::dos-tchechen-multipartite-boot-engine"
TCHECHEN_DISK_OVERWRITE = "objectives/impact/wipe/disk/mbr::dos-rtc-gated-partition-overwrite"
TCHECHEN_MBR_REWRITER = "objectives/impact/wipe/disk/mbr::dos-resident-mbr-partition-rewriter"
TCHECHEN_JUMP_WRITER = "objectives/impact/infect/binary/dos/com-bytes/file::dos-jump-prefixed-drop"
TCHECHEN_RELOCATION = "objectives/impact/infect/boot-sector::dos-boot-relocate-7c00-repne"
TCHECHEN_DAY_GATE = "objectives/impact/infect/boot-sector::dos-rtc-day16-boot-gate"
TCHECHEN_17_SECTOR_WRITE = "objectives/impact/infect/boot-sector::dos-bios-17-sector-write-loop"
BOOT_CRUEL_SHA256 = "011420d86e0c04c35256961f643c0db5ae581d635ecea3c07aa4056089fbd1c6"
BOOT_CRUEL_DISK_HOOK = "objectives/impact/infect/binary/dos/com-bytes/interrupt::dos-int13-hook-writer"
BOOT_CRUEL_SFT_INFECTOR = "objectives/impact/infect/binary/dos/sft::dos-sft-exec-infector"
BOOT_CRUEL_CMOS_TRIGGER = "objectives/impact/wipe/config::dos-cmos-day8-minute47-trigger"
BOOT_CRUEL_CMOS_CLEAR = "objectives/impact/wipe/config::dos-cmos-clear-hardware-config-checksum"
BOOT_CRUEL_CMOS_DESTRUCTION = "objectives/impact/wipe/config::dos-date-gated-cmos-config-destruction"
CASCADE_SHA256 = "4c94be82389ce3efadb8549bfd1ecfe0b0b68ae703d6471c363f17fa66e9df74"
CASCADE_DELTA = "objectives/anti-static/obfuscation/payload/polymorphic::dos-delta-offset-cx"
CASCADE_XOR = "objectives/anti-static/obfuscation/payload/polymorphic::dos-fixed-key-xor-overlap-word-si-loop"
CASCADE_ENCRYPTED = "objectives/anti-static/obfuscation/payload/polymorphic::dos-encrypted-virus-body"
CASCADE_INFECTOR = "objectives/impact/infect/binary/dos/com-bytes/file::dos-parasitic-encrypted-infector"
DIKSHEV_SHA256 = "d0b66dcd4ab07f0efa0e72d5a05c89b2005c16c0e7c00fdc65a6698970524f5d"
DIKSHEV_OPEN = "objectives/impact/infect/binary/dos/com-bytes/file::dos-open-update-inc-ax"
DIKSHEV_SEEK = "objectives/impact/infect/binary/dos/com-bytes/file::dos-seek-end-inc-ax"
DIKSHEV_FIND_NEXT = "objectives/impact/infect/binary/dos/com-bytes/interrupt::dos-int21-find-next-near-jump"
DIKSHEV_APPEND = "objectives/impact/infect/binary/dos/com-bytes/file::dos-relocated-append-infector"
DIKSHEV_DIRECTORY = "objectives/impact/infect/binary/dos/com-bytes/file::dos-com-directory-infector"
DIKSHEV_SEARCH_WRITE = "objectives/impact/infect/binary/dos/com-bytes/file::dos-com-first-match-overwriter"
SIRIUS_SHA256 = "95e99fe093b80886a64bb9cfc26f746383e14cf9908edc8b05d2e2c39fe42f30"
SIRIUS_DELTA = "objectives/anti-static/obfuscation/payload/polymorphic::dos-delta-offset-ax-to-bp"
SIRIUS_XOR = "objectives/anti-static/obfuscation/payload/polymorphic::dos-rolling-xor-word-loop"
SIRIUS_272_SHA256 = "4607f7ccf0ec1f711548f9137d322d483ee464cb5e6ff5c695da1177e3b04f3f"
SIRIUS_272_DELTA = "objectives/anti-static/obfuscation/payload/polymorphic::dos-delta-offset-bp-guarded"
SIRIUS_272_XOR = "objectives/anti-static/obfuscation/payload/polymorphic::dos-rolling-xor-word-count-loop"
SIRIUS_280_SHA256 = "c5365a4b62a92271246b298ff1f60bfa3ade946d8d664628c55bf937e524d561"
SIRIUS_280_DELTA = "objectives/anti-static/obfuscation/payload/polymorphic::dos-delta-offset-ax-to-bp"
SIRIUS_280_XOR = "objectives/anti-static/obfuscation/payload/polymorphic::dos-fixed-key-xor-word-copy-loop"
BW_LUDDITE_SHA256 = "4b8189e759e6d2353ae55a51081d6c5c93af170dcae53edf45b7c31bf8664526"
BW_LUDDITE_XOR = "objectives/anti-static/obfuscation/payload/polymorphic::dos-fixed-key-xor-word-bx-loop"
BW_LUDDITE_APPEND = "objectives/impact/infect/binary/dos/com-bytes/file::dos-relocated-append-infector"
BW_LUDDITE_TIME = "objectives/impact/infect/binary/dos/com-bytes/file::dos-timestamped-file-write"
BW_LUDDITE_DIRECTORY = "objectives/impact/infect/binary/dos/com-bytes/file::dos-com-directory-infector"
WON_SHA256 = "67ae9bdb7f420173c184ce1d6c97cc2b200034b9cdcde5204e8d45cdffe1bb9b"
WON_SECTOR = "objectives/impact/wipe/disk/raw::dos-int25-pre-data-sector"
WON_COUNTER = "objectives/impact/wipe/disk/raw::dos-int25-tail-marker-counter"
WON_ROOT_CORRUPTION = "objectives/impact/wipe/disk/raw::dos-int25-root-directory-tail-counter"
WON_EXEC_INFECTOR = "objectives/impact/infect/binary/dos/com-bytes/interrupt::dos-exec-hook-infector"
WON_PARASITIC_APPENDER = "objectives/impact/infect/binary/dos/exec-open-hook::dos-exec-hook-parasitic-appender"
RAPE_SHA256 = "198e1b10a7f437eab8675818d41584d4fc640ed47302d5847f6f325cae58df66"
RAPE_ROTATE = "objectives/anti-static/obfuscation/payload/polymorphic::dos-incrementing-ror-byte-loop"
RAPE_ENCRYPTED_INFECTOR = "objectives/anti-static/obfuscation/payload/polymorphic::dos-rotating-encrypted-virus-body"
RAPE_EXEC_INFECTOR = "objectives/impact/infect/binary/dos/com-bytes/interrupt::dos-exec-hook-infector"
RAPE_DISK_OVERWRITE = "objectives/impact/wipe/disk/mbr::dos-exec-virus-weekday-disk-overwrite"
EDDIE_SHA256 = "285f5fa31f65f60b558722128c9b982bd51345fe3ae3b2ae421d8a9a3c6b81e4"
EDDIE_INT8 = "objectives/impact/infect/binary/dos/com-bytes/interrupt::dos-int8-vector-install-direct"
EDDIE_DAY_GATE = "objectives/impact/ui/manipulation/harassment::dos-cmos-daymod4-gate"
EDDIE_EARLY_TICK = "objectives/impact/ui/manipulation/harassment::dos-int8-bda-early-tick-gate"
EDDIE_SPEAKER = "objectives/impact/ui/manipulation/harassment::dos-int8-pit-speaker-output"
EDDIE_SCREEN = "objectives/impact/ui/manipulation/harassment::dos-int8-vga-screen-save"
EDDIE_PRANK = "objectives/impact/ui/manipulation/harassment::dos-int8-rtc-gated-screen-speaker-prank"
WEEK_1614_SHA256 = "9c011b310d10727afa932006d4d85e9631242f7d90198440ca137b2422c155f7"
WEEK_1614_SEARCH_DISPATCH = "objectives/impact/infect/binary/dos/com-bytes/interrupt::dos-int21-table-directory-search-dispatch"
WEEK_1614_DTA_HIDE = "objectives/impact/infect/binary/dos/com-bytes/file::dos-dta-size-hide-si"
WEEK_1614_STEALTH = "objectives/impact/infect/binary/dos/com-bytes/interrupt::dos-int21-table-search-hook-hides-dta-size"
SOMEKIT_AOS_854_SHA256 = "b2d12238ebe9d62109929b9402f28076964722e4bffc8acf661e8494ad932d4f"
SOMEKIT_AOS_854_ADD_LOOP = "objectives/anti-static/obfuscation/payload/polymorphic::dos-additive-immediate-word-loop"
SOMEKIT_AOS_854_INFECTOR = "objectives/anti-static/obfuscation/payload/polymorphic::dos-additive-encrypted-infector"
SOMEKIT_AOS_854_DTA_HIDE = "objectives/impact/infect/binary/dos/com-bytes/file::dos-dta-size-hide-es-bx"
SOMEKIT_AOS_854_STEALTH = "objectives/impact/infect/binary/dos/com-bytes/interrupt::dos-int21-resident-search-hook-hides-body"
ALAR_4625_SHA256 = "d3c43299ea452c101a09a0d6bfc1b26fd321890b1d5f7a6115ae863f2b735f36"
ALAR_STAGE_LOADER = "objectives/impact/infect/boot-sector::dos-hidden-sector-stage-loader"
ALAR_BOOT_INSTALLER = "objectives/impact/infect/boot-sector::dos-partition-gated-hidden-sector-install"
ALAR_BOOT_INFECTOR = "objectives/impact/infect/boot-sector::dos-hidden-sector-mbr-infector"
ANTIFORT_1499_SHA256 = "f7f1cfe81a4077df4117b1b737b56537f7c45bfec3de8b57f1b1b9e213fc6db5"
ANTIFORT_1493_SHA256 = "7f59643339baf41f7258ea363a090314dfe177320d2259f3049cd6ebd673bb9e"
ANTIFORT_1499_XOR = "objectives/anti-static/obfuscation/payload/polymorphic::dos-fixed-key-stack-word-xor"
ANTIFORT_1499_INFECTOR = "objectives/anti-static/obfuscation/payload/polymorphic::dos-stack-xor-exec-infector"
ANTIPC_1958_SHA256 = "babb48ce355a431aab263a328cf7d5b79e835ac9f4c7879a3e9c377fe69373db"
ANTIPC_1958_XOR = "objectives/anti-static/obfuscation/payload/polymorphic::dos-appended-xor-bp-loop"
ANTIPC_1958_INFECTOR = "objectives/impact/infect/binary/dos/com-bytes/interrupt::dos-exec-hook-infector"
ASH_817_SHA256 = "3a34168bb4b407d8177a52e493dd526b1ee527126a3a88294368f9f446c8d5d5"
ASH_817_XOR = "objectives/anti-static/obfuscation/payload/polymorphic::dos-countdown-rotate-xor-loop"
ASH_817_INFECTOR = "objectives/impact/infect/binary/dos/com-bytes/file::dos-com-directory-infector"
ASH_817_DISK_WIPE = "objectives/impact/wipe/disk/mbr::dos-int26-calendar-gated-one-sector-wipe"
ASH_708_SHA256 = "fe3e378fa48c2c3baabe5c61dc2e3e2278ac74915b4a036d367792c11c369f2c"
ASH_708_XOR = "objectives/anti-static/obfuscation/payload/polymorphic::dos-appended-fixed-xor-bx-byte-loop"
ASH_708_INFECTOR = "objectives/impact/infect/binary/dos/com-bytes/file::dos-com-directory-infector"
LR_3728B_SHA256 = "3e4bcbfd8ec774eec9b16dc1586465d8ee6bf039822f684aa64531e01bb5f772"
LR_3728B_XOR = "objectives/anti-static/obfuscation/payload/polymorphic::dos-appended-two-stage-incrementing-xor"
LR_3728B_INFECTOR = "objectives/impact/infect/binary/dos/com-bytes/file::dos-relocated-append-infector"
LR_3728B_RESIDENT = "objectives/impact/infect/binary/dos/com-bytes/interrupt::dos-int21-resident-infector"
LR_3728B_VGA = "objectives/impact/ui/manipulation/harassment::dos-int1c-calendar-gated-vga-screen-prank"
ZAMOL_2153_SHA256 = "454321103f4d1c281515a0dded3cf0375fc2e8896c27600eb0b53f1d1c7c13b1"
ZAMOL_2153_XOR = "objectives/anti-static/obfuscation/payload/polymorphic::dos-discontiguous-fixed-xor-loop"
ZAMOL_2153_ENCRYPTED = "objectives/anti-static/obfuscation/payload/polymorphic::dos-encrypted-virus-body"
ZAMOL_2153_INFECTOR = "objectives/impact/infect/binary/dos/com-bytes/file::dos-relocated-append-infector"


def traits(binary: str, path: Path) -> dict[str, int]:
    result = subprocess.run(
        [binary, "--traits-dir", str(ROOT), "--format", "json", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(result.stdout)
    return {
        trait["id"]: trait["crit"]
        for file in report["files"]
        for trait in file.get("traits", [])
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()

    for name, digest in SAMPLES.items():
        sample = ROOT / "testdata/hostile/dos-com" / name
        actual = hashlib.sha256(sample.read_bytes()).hexdigest()
        assert actual == digest, f"{name} fixture changed: {actual}"
        matched = traits(args.cleave, sample)
        assert matched.get(WORD_XOR, 0) >= 3, (name, "missing word-XOR evidence", matched)
        assert matched.get(ENCRYPTED, 0) >= 5, (name, "missing encrypted-body finding", matched)
        assert matched.get(INFECTOR, 0) >= 5, (name, "missing infection finding", matched)
        print(f"{name}: passed", flush=True)

    nostardamus = ROOT / "testdata/hostile/dos-com/nostardamus-1870"
    actual = hashlib.sha256(nostardamus.read_bytes()).hexdigest()
    assert actual == NOSTARDAMUS_SHA256, f"nostardamus fixture changed: {actual}"
    matched = traits(args.cleave, nostardamus)
    assert matched.get(NOSTARDAMUS_INFECTOR, 0) >= 5, (
        "Nostardamus did not expose its decoded resident infection behavior",
        matched,
    )
    for trait_id in (NOSTARDAMUS_HIDDEN_APPEND, NOSTARDAMUS_SEARCH_HOOK):
        assert matched.get(trait_id, 0) >= 5, ("Nostardamus missed a hostile behavior composite", trait_id, matched)
    print("nostardamus-1870: passed", flush=True)

    fulldead = ROOT / "testdata/hostile/dos-com/fulldead-503"
    actual = hashlib.sha256(fulldead.read_bytes()).hexdigest()
    assert actual == FULLDEAD_SHA256, f"fulldead fixture changed: {actual}"
    matched = traits(args.cleave, fulldead)
    assert matched.get(FULLDEAD_FILE_INFECTOR, 0) >= 5, (
        "FullDead did not expose its decoded COM infection behavior",
        matched,
    )
    assert matched.get(FULLDEAD_DISK_INFECTOR, 0) >= 5, (
        "FullDead did not expose its low-memory multi-sector BIOS write",
        matched,
    )
    assert matched.get(FULLDEAD_DISK_GATE, 0) >= 4, (
        "FullDead's infection-count disk trigger was not recovered",
        matched,
    )
    print("fulldead-503: passed", flush=True)

    tchechen = ROOT / "testdata/hostile/dos-com/tchechen-3370"
    actual = hashlib.sha256(tchechen.read_bytes()).hexdigest()
    assert actual == TCHECHEN_SHA256, f"tchechen fixture changed: {actual}"
    matched = traits(args.cleave, tchechen)
    for trait_id in (
        TCHECHEN_BOOT_ENGINE,
        TCHECHEN_DISK_OVERWRITE,
        TCHECHEN_MBR_REWRITER,
        TCHECHEN_JUMP_WRITER,
        TCHECHEN_RELOCATION,
        TCHECHEN_DAY_GATE,
        TCHECHEN_17_SECTOR_WRITE,
    ):
        assert matched.get(trait_id, 0) >= (
            5
            if trait_id
            in (
                TCHECHEN_BOOT_ENGINE,
                TCHECHEN_DISK_OVERWRITE,
                TCHECHEN_MBR_REWRITER,
                TCHECHEN_JUMP_WRITER,
            )
            else 4
        ), (
            "Tchechen decoded boot behavior missing",
            trait_id,
            matched,
        )
    assert sum(crit >= 5 for crit in matched.values()) >= 4, (
        "Tchechen did not produce four independent hostile behaviors",
        matched,
    )
    print("tchechen-3370: passed", flush=True)

    boot_cruel = ROOT / "testdata/hostile/dos-com/boot-cruel-1022"
    actual = hashlib.sha256(boot_cruel.read_bytes()).hexdigest()
    assert actual == BOOT_CRUEL_SHA256, f"boot-cruel fixture changed: {actual}"
    matched = traits(args.cleave, boot_cruel)
    for trait_id in (
        BOOT_CRUEL_DISK_HOOK,
        BOOT_CRUEL_SFT_INFECTOR,
        BOOT_CRUEL_CMOS_TRIGGER,
        BOOT_CRUEL_CMOS_CLEAR,
        BOOT_CRUEL_CMOS_DESTRUCTION,
    ):
        assert matched.get(trait_id, 0) >= (5 if trait_id in (
            BOOT_CRUEL_DISK_HOOK,
            BOOT_CRUEL_SFT_INFECTOR,
            BOOT_CRUEL_CMOS_DESTRUCTION,
        ) else 4), ("Boot.Cruel behavior missing", trait_id, matched)
    assert sum(crit >= 5 for crit in matched.values()) >= 3, (
        "Boot.Cruel did not produce three distinct hostile findings",
        matched,
    )
    print("boot-cruel-1022: passed", flush=True)

    cascade = ROOT / "testdata/hostile/dos-com/cascade-1701e"
    actual = hashlib.sha256(cascade.read_bytes()).hexdigest()
    assert actual == CASCADE_SHA256, f"cascade fixture changed: {actual}"
    matched = traits(args.cleave, cascade)
    for trait_id in (CASCADE_DELTA, CASCADE_XOR):
        assert matched.get(trait_id, 0) >= 3, ("Cascade decoder evidence missing", trait_id, matched)
    for trait_id in (CASCADE_ENCRYPTED, CASCADE_INFECTOR):
        assert matched.get(trait_id, 0) >= 5, ("Cascade encrypted infector finding missing", trait_id, matched)
    print("cascade-1701e: passed", flush=True)

    dikshev = ROOT / "testdata/hostile/dos-com/dikshev-192b"
    actual = hashlib.sha256(dikshev.read_bytes()).hexdigest()
    assert actual == DIKSHEV_SHA256, f"Dikshev fixture changed: {actual}"
    matched = traits(args.cleave, dikshev)
    for trait_id in (DIKSHEV_OPEN, DIKSHEV_SEEK, DIKSHEV_FIND_NEXT):
        assert matched.get(trait_id, 0) >= 3, ("Dikshev obfuscated DOS service missing", trait_id, matched)
    for trait_id in (DIKSHEV_APPEND, DIKSHEV_DIRECTORY, DIKSHEV_SEARCH_WRITE):
        assert matched.get(trait_id, 0) >= 5, ("Dikshev infection behavior missing", trait_id, matched)
    print("dikshev-192b: passed", flush=True)

    sirius = ROOT / "testdata/hostile/dos-com/sirius-annihilator-711"
    actual = hashlib.sha256(sirius.read_bytes()).hexdigest()
    assert actual == SIRIUS_SHA256, f"Sirius fixture changed: {actual}"
    matched = traits(args.cleave, sirius)
    for trait_id in (SIRIUS_DELTA, SIRIUS_XOR):
        assert matched.get(trait_id, 0) >= 3, ("Sirius decoder evidence missing", trait_id, matched)
    for trait_id in (ENCRYPTED, INFECTOR):
        assert matched.get(trait_id, 0) >= 5, ("Sirius encrypted infector finding missing", trait_id, matched)
    print("sirius-annihilator-711: passed", flush=True)

    for name, digest, delta_id, xor_id in (
        ("sirius-annihilator-272d", SIRIUS_272_SHA256, SIRIUS_272_DELTA, SIRIUS_272_XOR),
        ("sirius-annihilator-280", SIRIUS_280_SHA256, SIRIUS_280_DELTA, SIRIUS_280_XOR),
    ):
        sample = ROOT / "testdata/hostile/dos-com" / name
        actual = hashlib.sha256(sample.read_bytes()).hexdigest()
        assert actual == digest, f"{name} fixture changed: {actual}"
        matched = traits(args.cleave, sample)
        for trait_id in (delta_id, xor_id):
            assert matched.get(trait_id, 0) >= 3, (f"{name} decoder evidence missing", trait_id, matched)
        for trait_id in (ENCRYPTED, INFECTOR):
            assert matched.get(trait_id, 0) >= 5, (f"{name} encrypted infector finding missing", trait_id, matched)
        print(f"{name}: passed", flush=True)

    bw_luddite = ROOT / "testdata/hostile/dos-com/bw-luddite-1346"
    actual = hashlib.sha256(bw_luddite.read_bytes()).hexdigest()
    assert actual == BW_LUDDITE_SHA256, f"BW.Luddite fixture changed: {actual}"
    matched = traits(args.cleave, bw_luddite)
    assert matched.get(BW_LUDDITE_XOR, 0) >= 3, ("BW.Luddite decoder evidence missing", matched)
    for trait_id in (BW_LUDDITE_APPEND, BW_LUDDITE_TIME, BW_LUDDITE_DIRECTORY):
        assert matched.get(trait_id, 0) >= 5, ("BW.Luddite infection behavior missing", trait_id, matched)
    print("bw-luddite-1346: passed", flush=True)

    won = ROOT / "testdata/hostile/dos-com/won-2339"
    actual = hashlib.sha256(won.read_bytes()).hexdigest()
    assert actual == WON_SHA256, f"Won fixture changed: {actual}"
    matched = traits(args.cleave, won)
    for trait_id in (WON_SECTOR, WON_COUNTER):
        assert matched.get(trait_id, 0) >= 3, ("Won disk-counter evidence missing", trait_id, matched)
    for trait_id in (WON_ROOT_CORRUPTION, WON_EXEC_INFECTOR, WON_PARASITIC_APPENDER):
        assert matched.get(trait_id, 0) >= 5, ("Won infection or directory-corruption behavior missing", trait_id, matched)
    assert sum(crit >= 5 for crit in matched.values()) >= 3, (
        "Won did not produce three independent hostile findings",
        matched,
    )
    print("won-2339: passed", flush=True)

    rape = ROOT / "testdata/hostile/dos-com/rape-2496"
    actual = hashlib.sha256(rape.read_bytes()).hexdigest()
    assert actual == RAPE_SHA256, f"Rape fixture changed: {actual}"
    matched = traits(args.cleave, rape)
    assert matched.get(RAPE_ROTATE, 0) >= 3, ("Rape rotating decoder evidence missing", matched)
    for trait_id in (RAPE_ENCRYPTED_INFECTOR, RAPE_EXEC_INFECTOR, RAPE_DISK_OVERWRITE):
        assert matched.get(trait_id, 0) >= 5, ("Rape infection or disk-overwrite behavior missing", trait_id, matched)
    assert sum(crit >= 5 for crit in matched.values()) >= 3, (
        "Rape did not produce three distinct hostile findings",
        matched,
    )
    for trait_id in (EDDIE_INT8, EDDIE_DAY_GATE, EDDIE_EARLY_TICK, EDDIE_SPEAKER, EDDIE_SCREEN, EDDIE_PRANK):
        assert trait_id not in matched, ("Rape matched Eddie's timer prank", trait_id, matched)
    print("rape-2496: passed", flush=True)

    eddie = ROOT / "testdata/hostile/dos-com/eddie-2104"
    actual = hashlib.sha256(eddie.read_bytes()).hexdigest()
    assert actual == EDDIE_SHA256, f"Eddie fixture changed: {actual}"
    matched = traits(args.cleave, eddie)
    for trait_id in (EDDIE_INT8, EDDIE_DAY_GATE, EDDIE_EARLY_TICK, EDDIE_SCREEN):
        assert matched.get(trait_id, 0) >= 3, ("Eddie timer payload evidence missing", trait_id, matched)
    for trait_id in (EDDIE_SPEAKER, EDDIE_PRANK, RAPE_EXEC_INFECTOR):
        assert matched.get(trait_id, 0) >= (5 if trait_id == RAPE_EXEC_INFECTOR else 4), (
            "Eddie prank or infector behavior missing", trait_id, matched
        )
    print("eddie-2104: passed", flush=True)

    week = ROOT / "testdata/hostile/dos-com/week-1614"
    actual = hashlib.sha256(week.read_bytes()).hexdigest()
    assert actual == WEEK_1614_SHA256, f"Week.1614 fixture changed: {actual}"
    matched = traits(args.cleave, week)
    for trait_id in (WEEK_1614_SEARCH_DISPATCH, WEEK_1614_DTA_HIDE):
        assert matched.get(trait_id, 0) >= 3, ("Week.1614 behavior evidence missing", trait_id, matched)
    assert matched.get(WEEK_1614_STEALTH, 0) >= 5, (
        "Week.1614's resident search hook did not expose DTA size stealth",
        matched,
    )
    print("week-1614: passed", flush=True)

    somekit = ROOT / "testdata/hostile/dos-com/somekit-aos-854"
    actual = hashlib.sha256(somekit.read_bytes()).hexdigest()
    assert actual == SOMEKIT_AOS_854_SHA256, f"SomeKit.AOS.854 fixture changed: {actual}"
    matched = traits(args.cleave, somekit)
    assert matched.get(SOMEKIT_AOS_854_ADD_LOOP, 0) >= 3, (
        "SomeKit.AOS.854 additive decryptor missing",
        matched,
    )
    assert matched.get(SOMEKIT_AOS_854_INFECTOR, 0) >= 5, (
        "SomeKit.AOS.854 decoded infector behavior missing",
        matched,
    )
    assert matched.get(SOMEKIT_AOS_854_DTA_HIDE, 0) >= 3, (
        "SomeKit.AOS.854 DTA concealment evidence missing",
        matched,
    )
    assert matched.get(SOMEKIT_AOS_854_STEALTH, 0) >= 5, (
        "SomeKit.AOS.854 directory stealth behavior missing",
        matched,
    )
    print("somekit-aos-854: passed", flush=True)

    alar = ROOT / "testdata/hostile/dos-com/alar-4625"
    actual = hashlib.sha256(alar.read_bytes()).hexdigest()
    assert actual == ALAR_4625_SHA256, f"Alar fixture changed: {actual}"
    matched = traits(args.cleave, alar)
    for trait_id in (ALAR_STAGE_LOADER, ALAR_BOOT_INSTALLER, ALAR_BOOT_INFECTOR):
        assert matched.get(trait_id, 0) >= (5 if trait_id == ALAR_BOOT_INFECTOR else 4), (
            "Alar hidden-sector boot behavior missing",
            trait_id,
            matched,
        )
    print("alar-4625: passed", flush=True)

    antifort = ROOT / "testdata/hostile/dos-com/antifort-1499"
    actual = hashlib.sha256(antifort.read_bytes()).hexdigest()
    assert actual == ANTIFORT_1499_SHA256, f"AntiFort fixture changed: {actual}"
    matched = traits(args.cleave, antifort)
    assert matched.get(ANTIFORT_1499_XOR, 0) >= 4, (
        "AntiFort's fixed-key word decoder was not identified",
        matched,
    )
    assert matched.get(ANTIFORT_1499_INFECTOR, 0) >= 5, (
        "AntiFort's encrypted execution hook and file infection were not joined",
        matched,
    )
    print("antifort-1499: passed", flush=True)

    antifort = ROOT / "testdata/hostile/dos-com/antifort-1493"
    actual = hashlib.sha256(antifort.read_bytes()).hexdigest()
    assert actual == ANTIFORT_1493_SHA256, f"AntiFort.1493 fixture changed: {actual}"
    matched = traits(args.cleave, antifort)
    assert matched.get(ANTIFORT_1499_XOR, 0) >= 4, (
        "AntiFort.1493's fixed-key word decoder was not identified",
        matched,
    )
    assert matched.get(ANTIFORT_1499_INFECTOR, 0) >= 5, (
        "AntiFort.1493's encrypted execution hook and file infection were not joined",
        matched,
    )
    print("antifort-1493: passed", flush=True)

    antipc = ROOT / "testdata/hostile/dos-com/antipc-1958"
    actual = hashlib.sha256(antipc.read_bytes()).hexdigest()
    assert actual == ANTIPC_1958_SHA256, f"AntiPC fixture changed: {actual}"
    matched = traits(args.cleave, antipc)
    assert matched.get(ANTIPC_1958_XOR, 0) >= 4, (
        "AntiPC's appended byte-XOR loader was not identified",
        matched,
    )
    assert matched.get(ANTIPC_1958_INFECTOR, 0) >= 5, (
        "AntiPC's decoded execution hook and file infection were not identified",
        matched,
    )
    print("antipc-1958: passed", flush=True)

    ash = ROOT / "testdata/hostile/dos-com/ash-817"
    actual = hashlib.sha256(ash.read_bytes()).hexdigest()
    assert actual == ASH_817_SHA256, f"Ash.817 fixture changed: {actual}"
    matched = traits(args.cleave, ash)
    assert matched.get(ASH_817_XOR, 0) >= 4, (
        "Ash.817's countdown-rotated decryptor was not identified",
        matched,
    )
    assert matched.get(ASH_817_INFECTOR, 0) >= 5, (
        "Ash.817's decoded COM directory infection was not identified",
        matched,
    )
    assert matched.get(ASH_817_DISK_WIPE, 0) >= 5, (
        "Ash.817's date-triggered absolute disk write was not identified",
        matched,
    )
    print("ash-817: passed", flush=True)

    ash = ROOT / "testdata/hostile/dos-com/ash-708"
    actual = hashlib.sha256(ash.read_bytes()).hexdigest()
    assert actual == ASH_708_SHA256, f"Ash.708 fixture changed: {actual}"
    matched = traits(args.cleave, ash)
    assert matched.get(ASH_708_XOR, 0) >= 4, (
        "Ash.708's appended fixed-key byte-XOR loader was not identified",
        matched,
    )
    assert matched.get(ASH_708_INFECTOR, 0) >= 5, (
        "Ash.708's decoded COM directory infection was not identified",
        matched,
    )
    print("ash-708: passed", flush=True)

    lr_3728b = ROOT / "testdata/hostile/dos-com/lr-3728b"
    actual = hashlib.sha256(lr_3728b.read_bytes()).hexdigest()
    assert actual == LR_3728B_SHA256, f"LR.3728.b fixture changed: {actual}"
    matched = traits(args.cleave, lr_3728b)
    assert matched.get(LR_3728B_XOR, 0) >= 4, (
        "LR.3728.b's two-stage incremental-XOR loader was not identified",
        matched,
    )
    assert matched.get(LR_3728B_INFECTOR, 0) >= 5, (
        "LR.3728.b's decoded relocated file infection was not identified",
        matched,
    )
    assert matched.get(LR_3728B_RESIDENT, 0) >= 5, (
        "LR.3728.b's resident INT 21h infection hook was not identified",
        matched,
    )
    assert matched.get(LR_3728B_VGA, 0) >= 4, (
        "LR.3728.b's calendar-gated VGA effect was not identified",
        matched,
    )
    print("lr-3728b: passed", flush=True)

    zamol_2153 = ROOT / "testdata/hostile/dos-com/zamol-2153"
    actual = hashlib.sha256(zamol_2153.read_bytes()).hexdigest()
    assert actual == ZAMOL_2153_SHA256, f"Zamol.2153 fixture changed: {actual}"
    matched = traits(args.cleave, zamol_2153)
    assert matched.get(ZAMOL_2153_XOR, 0) >= 4, (
        "Zamol.2153's discontiguous fixed-XOR decoder was not identified",
        matched,
    )
    assert matched.get(ZAMOL_2153_ENCRYPTED, 0) >= 5, (
        "Zamol.2153's encrypted resident body was not identified",
        matched,
    )
    assert matched.get(ZAMOL_2153_INFECTOR, 0) >= 5, (
        "Zamol.2153's decoded file infection was not identified",
        matched,
    )
    print("zamol-2153: passed", flush=True)

    for name in (
        "dos-table-query.com",
        "dos-ah52-unrelated-call.com",
        "anton-97",
        "artem-2165",
    ):
        folder = "testdata/hostile/dos-com" if name in ("anton-97", "artem-2165") else "testdata/benign"
        matched = traits(args.cleave, ROOT / folder / name)
        for trait_id in (
            WORD_XOR,
            ENCRYPTED,
            INFECTOR,
            CASCADE_DELTA,
            CASCADE_XOR,
            CASCADE_ENCRYPTED,
            CASCADE_INFECTOR,
            SOMEKIT_AOS_854_ADD_LOOP,
            SOMEKIT_AOS_854_INFECTOR,
            SOMEKIT_AOS_854_DTA_HIDE,
            SOMEKIT_AOS_854_STEALTH,
            ALAR_STAGE_LOADER,
            ALAR_BOOT_INSTALLER,
            ALAR_BOOT_INFECTOR,
            ANTIFORT_1499_XOR,
            ANTIFORT_1499_INFECTOR,
        ):
            assert trait_id not in matched, (name, "control matched", trait_id, matched)
        for trait_id in (NOSTARDAMUS_INFECTOR, NOSTARDAMUS_HIDDEN_APPEND, NOSTARDAMUS_SEARCH_HOOK):
            assert trait_id not in matched, (name, "Nostardamus control matched", trait_id, matched)
        for trait_id in (FULLDEAD_FILE_INFECTOR, FULLDEAD_DISK_INFECTOR, FULLDEAD_DISK_GATE):
            assert trait_id not in matched, (name, "FullDead control matched", trait_id, matched)
        for trait_id in (
            TCHECHEN_BOOT_ENGINE,
            TCHECHEN_DISK_OVERWRITE,
            TCHECHEN_MBR_REWRITER,
            TCHECHEN_JUMP_WRITER,
            TCHECHEN_RELOCATION,
            TCHECHEN_DAY_GATE,
            TCHECHEN_17_SECTOR_WRITE,
        ):
            assert trait_id not in matched, (name, "Tchechen control matched", trait_id, matched)
        for trait_id in (
            BOOT_CRUEL_SFT_INFECTOR,
            BOOT_CRUEL_CMOS_TRIGGER,
            BOOT_CRUEL_CMOS_CLEAR,
            BOOT_CRUEL_CMOS_DESTRUCTION,
        ):
            assert trait_id not in matched, (name, "Boot.Cruel control matched", trait_id, matched)
        for trait_id in (DIKSHEV_OPEN, DIKSHEV_SEEK, DIKSHEV_FIND_NEXT, DIKSHEV_APPEND, DIKSHEV_DIRECTORY):
            assert trait_id not in matched, (name, "Dikshev control matched", trait_id, matched)
        for trait_id in (
            SIRIUS_DELTA,
            SIRIUS_XOR,
            SIRIUS_272_DELTA,
            SIRIUS_272_XOR,
            SIRIUS_280_DELTA,
            SIRIUS_280_XOR,
            BW_LUDDITE_XOR,
            ENCRYPTED,
            INFECTOR,
        ):
            assert trait_id not in matched, (name, "Sirius control matched", trait_id, matched)
        for trait_id in (WON_SECTOR, WON_COUNTER, WON_ROOT_CORRUPTION, WON_PARASITIC_APPENDER,
                         RAPE_ROTATE, RAPE_ENCRYPTED_INFECTOR, RAPE_DISK_OVERWRITE,
                         EDDIE_INT8, EDDIE_DAY_GATE, EDDIE_EARLY_TICK, EDDIE_SPEAKER, EDDIE_SCREEN, EDDIE_PRANK):
            assert trait_id not in matched, (name, "Won-specific behavior matched", trait_id, matched)
        print(f"{name}: passed", flush=True)


if __name__ == "__main__":
    main()
