#!/usr/bin/env python3
"""Check Makefile triage findings and target parsing without running recipes."""

import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile


COMPILE = "micro-behaviors/metaprogramming/generation/compile::makefile-"
NATIVE = COMPILE + "native-compiler-variable-recipe"
JAVA = COMPILE + "java-compiler-variable-recipe"
KOTLIN = COMPILE + "kotlin-compiler-variable-recipe"
LIBS = "metadata/build/make::linker-library-flags-assignment"
TARGET = "metadata/build/makefile-shape::"
TARGETS = {name: TARGET + name + "-target-assignment"
           for name in ("all", "install", "clean", "distclean", "dep")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="../cleave/target/release/cleave")
    parser.add_argument("--samples", type=Path, help="Optional original triage sample directory")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    engine = str((repo / args.cleave).resolve())
    fixtures = {
        "native.mk": ("CC = clang\nall:\n\t$(CC) $(CFLAGS) -o $@ $<\n", {NATIVE}),
        "cxx.mk": ("CXX = c++\nall:\n\t-@${CXX} -o app main.cpp\n", {NATIVE}),
        "prefix-space.mk": ("CC = cc\nall:\n\t @+ $(CC) -o app main.c\n", {NATIVE}),
        "java.mk": ("JAVAC := javac\nall:\n\t+@$(JAVAC) -d build Main.java\n", {JAVA}),
        "kotlin.mk": ("KOTLIN := kotlinc\nall:\n\t@ ${KOTLIN} Main.kt -d app.jar\n", {KOTLIN}),
        "crlf.mk": ("CC=cc\r\nall:\r\n\t$(CC) -o app main.c\r\n", {NATIVE}),
        "binding.mk": ("CC = gcc\nCXX = c++\nJAVAC = javac\nKOTLIN = kotlinc\n", set()),
        "comment.mk": ("#\t$(CC) -o app main.c\nall:\n\t# $(JAVAC) Main.java\n", set()),
        "echo.mk": ("all:\n\t@echo '$(CC) $(JAVAC) $(KOTLIN)'\n", set()),
        "bad-delimiter.mk": ("all:\n\t$(CC} -o app main.c\n", set()),
        "libs.mk": ("LDFLAGS=-lX11\n", {LIBS}),
        "ldlibs.mk": ("LDLIBS ?= -L/usr/lib -lsocket -lnsl\n", {LIBS}),
        "append.mk": ("LDFLAGS += $(EXTRA) -ldl -lkvm\n", {LIBS}),
        "lib-comment.mk": ("# LDFLAGS=-lX11\nLDFLAGS = -L/usr/lib # -lkvm\n", set()),
        "lib-prefix.mk": ("EXTRA_LDFLAGS = -lX11\n", set()),
        "lib-path.mk": ("LDFLAGS = -Wl,--library-path=/usr/lib\n", set()),
        "lib-echo.mk": ("all:\n\t@echo 'LDFLAGS = -lX11'\n", set()),
    }
    layouts = {
        "target-list.mk": ("all install clean distclean dep:\n\t@echo done\n", set(TARGETS)),
        "target-tabs.mk": ("all\tinstall\tclean\tdistclean\tdep:\n\t@echo done\n", set(TARGETS)),
        "target-suffix.mk": ("uninstall:\n\t@echo done\ndistclean:\n\t@echo done\nsmall:\n\t@echo done\nnodep:\n\t@echo done\n", {"distclean"}),
        "target-comment.mk": ("# all:\n# install:\n# clean:\n# distclean:\n# dep:\nTEXT = clean:\ncheck:\n\t@echo 'install:'\n", set()),
        "target-bind.mk": ("all := text\ninstall ::= text\nclean := text\ndistclean := text\ndep := text\n", set()),
        "target-space.mk": ("all :\n\t@echo done\nclean ::\n\t@echo done\ninstall: ; @echo done\ndep:\n\t@echo done\ndistclean:\n\t@echo done\n", set(TARGETS)),
        "target-group.mk": ("all install &: input\n\t@echo done\n", {"all", "install"}),
    }
    with tempfile.TemporaryDirectory(prefix="makefile-triage-controls-") as directory:
        work = Path(directory)
        for name, (content, _) in {**fixtures, **layouts}.items():
            (work / name).write_bytes(content.encode())
        expected = {name: ids for name, (_, ids) in fixtures.items()}
        if args.samples:
            for source in sorted(args.samples.rglob("*")):
                if not source.is_file():
                    continue
                content = source.read_bytes()
                compiler = KOTLIN if b"$(KOTLIN)" in content else JAVA if b"$(JAVAC)" in content else NATIVE
                for basename in ("Makefile", "unrelated.mk"):
                    name = source.name + "/" + basename
                    dest = work / name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(content)
                    expected[name] = {compiler}
        result = subprocess.run(
            [engine, "--traits-dir", str(repo), "--all-files", "--format", "json", str(work)],
            check=True, text=True, capture_output=True,
        )
        assert "skipped trait file" not in result.stderr, result.stderr
        files = {str(Path(f["path"]).relative_to(work)): f
                 for line in result.stdout.splitlines() if line.strip()
                 for f in json.loads(line)["files"]}
        assert len(files) == len(expected) + len(layouts), files.keys()
        for name, file in files.items():
            traits = file.get("traits", [])
            assert file["type"] == "makefile", (name, file["type"])
            assert not [t for t in traits if t["crit"] >= 4], (name, traits)
            if name in expected:
                observed = {t["id"] for t in traits} & {NATIVE, JAVA, KOTLIN, LIBS}
                if name in fixtures:
                    assert observed == expected[name], (name, observed, expected[name])
                else:
                    assert expected[name] <= observed, (name, observed, expected[name])
        # Baselines may be omitted from JSON. Check actual rule matching as
        # well as output, so a misleading low-criticality match cannot hide.
        for name, (_, targets) in layouts.items():
            result = subprocess.run(
                [engine, "--traits-dir", str(repo), "test-rules", str(work / name),
                 "--rules", ",".join(TARGETS.values())],
                check=True, text=True, capture_output=True,
            )
            observed = set(re.findall(r"^MATCHED (\S+)", result.stdout, re.MULTILINE))
            required = {TARGETS[target] for target in targets}
            assert observed == required, (name, observed, required, result.stdout)
        print(f"PASS: {len(files)} Makefiles; {len(layouts)} target matching controls")


if __name__ == "__main__":
    main()
