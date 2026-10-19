"""Static controls. Specimens and mutations stay in the supplied work directory."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import struct
import subprocess

import pefile

ROOT = Path(__file__).resolve().parents[3]
POP3 = "micro-behaviors/communications/email/access/pop3::"
CHILD = "micro-behaviors/process/create/subprocess::"
HOSTILE_GO = {
    "objectives/execution/payload/file-exec::go-powershell-certutil-stage",
    "objectives/evasion/security-bypass/policy/execution::go-hidden-powershell-policy-bypass",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native", type=Path, required=True)
    parser.add_argument("--bot", type=Path, required=True)
    parser.add_argument("--go-source", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    cases = []

    def case(name, data, required=(), forbidden=()):
        cases.append((name, data, set(required), set(forbidden)))

    native = args.native.read_bytes()
    wire = (b"RETR %d\r\n\0", b"UIDL\r\n\0")
    for token in wire:
        assert native.count(token) == 1
    case("unnamed-section.exe", native, [POP3 + "native-retrieval-command-set"])
    case("no-uidl-command.exe", native.replace(wire[1], bytes(len(wire[1]))),
         forbidden=[POP3 + "native-retrieval-command-set"])
    stripped = native
    for token in wire:
        stripped = stripped.replace(token, bytes(len(token)))
    case("overlay-only-commands.exe", stripped + b"".join(wire), forbidden=[
        POP3 + "numbered-retr-command-template", POP3 + "uidl-command",
        POP3 + "native-retrieval-command-set"])
    # Change the actual section-table name, not an unrelated string.
    pe = struct.unpack_from("<I", native, 0x3c)[0]
    section_table = pe + 24 + struct.unpack_from("<H", native, pe + 20)[0]
    assert native[section_table] == 0
    named = bytearray(native)
    named[section_table:section_table + 8] = b".text\0\0\0"
    case("named-section.exe", bytes(named), [POP3 + "native-retrieval-command-set"])
    # Named imports must retain the coverage that existed before ordinal support.
    image = pefile.PE(data=native, fast_load=True)
    image.parse_data_directories(directories=[1])
    by_name = bytearray(native)
    spare = image.sections[2]
    offset = spare.PointerToRawData
    names = {16: b"recv", 19: b"send", 4: b"connect", 23: b"socket"}
    for library in image.DIRECTORY_ENTRY_IMPORT:
        if library.dll.lower() != b"ws2_32.dll":
            continue
        for imp in library.imports:
            if imp.ordinal not in names:
                continue
            entry = b"\0\0" + names[imp.ordinal] + b"\0"
            rva = spare.VirtualAddress + offset - spare.PointerToRawData
            by_name[offset:offset + len(entry)] = entry
            struct.pack_into("<I", by_name, imp.thunk_offset, rva)
            struct.pack_into("<I", by_name, image.get_offset_from_rva(imp.address - image.OPTIONAL_HEADER.ImageBase), rva)
            offset += len(entry) + 2
    case("named-winsock-imports.exe", bytes(by_name), [POP3 + "native-retrieval-command-set"])

    # Preserve the observed PowerShell string, but use only one main function.
    line = next(x for x in args.go_source.read_text().splitlines() if "exec.Command" in x)
    assert line.rstrip().endswith(").Run()")

    def source(command):
        return ('package main\nimport "os/exec"\nfunc main() {\n' + command + '\n}\n').encode()

    case("concealed-run.go", source(line), HOSTILE_GO | {CHILD + "go-powershell-launch-call"})
    case("concealed-start.go", source(line.replace(".Run()", ".Start()")), HOSTILE_GO)
    case("constructor-only.go", source(line.replace(".Run()", "")),
         [CHILD + "go-powershell-command"], HOSTILE_GO | {CHILD + "go-powershell-launch-call"})
    case("unrelated-command-runs.go", source(line.replace(".Run()", "") + '\nexec.Command("echo", "hello").Run()'),
         [CHILD + "go-powershell-command"], HOSTILE_GO | {CHILD + "go-powershell-launch-call"})
    case("powershell-is-an-argument.go", source(line.replace('(\"powershell\",', '(\"echo\", \"powershell\",', 1)),
         forbidden=HOSTILE_GO | {CHILD + "go-powershell-command"})
    case("visible-run.go", source(line.replace(" " * 1832, " ")),
         [CHILD + "go-powershell-launch-call"], HOSTILE_GO)
    case("commented-payload.go", source("// " + line),
         forbidden=HOSTILE_GO | {CHILD + "go-powershell-command", CHILD + "go-powershell-launch-call"})

    stream = "micro-behaviors/process/fd/stdio::python-stdin-from-stdout-attribute"
    case("stdin-stdout.py", b"configure(stdin=child.stdout)\n", [stream],
         [CHILD + "python-child-stdout-as-stdin"])
    case("stdin-other.py", b"configure(stdin=child.input)\n", forbidden=[stream])
    case("popen-import-only.py", b"from subprocess import Popen\n",
         forbidden=[CHILD + "popen-import", CHILD + "popen-ast"])
    transfer = "micro-behaviors/process/io/stream::"
    case("received-to-stdin.py", b"child.stdin.write(peer.recv(4096))\n",
         [transfer + "python-received-data-to-stdin"],
         [transfer + "python-standard-output-to-send"])
    case("stdout-to-peer.py", b"peer.send(child.stdout.read(4096))\n",
         [transfer + "python-standard-output-to-send"],
         [transfer + "python-received-data-to-stdin"])
    case("independent-streams.py", b"data = peer.recv(4096)\nchild.stdin.write(other)\n",
         forbidden=[transfer + "python-received-data-to-stdin"])

    bot = args.bot.read_bytes()
    receive = "micro-behaviors/communications/socket/receive::x86-recv-buffer-task-dispatch"
    objectives = {
        "objectives/impact/degrade/edr/targeting::socket-tasking-security-process-killer",
        "objectives/impact/system/shutdown::forced-reboot-pe",
    }
    case("bot-original.exe", bot, objectives | {receive})
    assert bot[0x6f7d:0x6f7e] == b"\x53"
    modified = bot[:0x6f7d] + b"\x90" * 65 + bot[0x6f7d + 65:]
    case("bot-without-receive-dispatch.exe", modified, forbidden=objectives | {receive})

    def scan(item):
        name, data, required, forbidden = item
        path = args.work_dir / name
        path.write_bytes(data)
        result = subprocess.run([args.cleave, "--traits-dir", str(ROOT), "--format", "json", str(path)],
                                check=True, capture_output=True, text=True)
        report = json.loads(result.stdout)
        found = {t["id"] for f in report["files"] for t in f.get("traits", [])}
        assert required <= found, (name, "missing", sorted(required - found))
        assert not forbidden & found, (name, "unexpected", sorted(forbidden & found))
        return {"case": name, "passed": True, "required": sorted(required),
                "forbidden": sorted(forbidden)}

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(scan, cases))
    output = {"passed": len(results), "total": len(cases), "cases": results}
    (args.work_dir / "results.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"passed": len(results), "total": len(cases)}))


if __name__ == "__main__":
    main()
