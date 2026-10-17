#!/usr/bin/env bash
set -euo pipefail

fixture_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
build_dir="$(mktemp -d)"
trap 'rm -rf "$build_dir"' EXIT

clang_bin="${CLANG:-clang}"
link_bin="${LLD_LINK:-lld-link}"
dlltool_bin="${LLVM_DLLTOOL:-llvm-dlltool}"
rc_bin="${LLVM_RC:-llvm-rc}"

make_import_lib() {
  local base="$1" library="$2"
  shift 2
  {
    printf 'LIBRARY %s\nEXPORTS\n' "$library"
    for symbol in "$@"; do printf ' %s\n' "$symbol"; done
  } > "$build_dir/$base.def"
  "$dlltool_bin" -m i386:x86-64 -d "$build_dir/$base.def" -l "$build_dir/$base.lib"
}

make_import_lib kernel32 KERNEL32.dll CreateMutexA CreateFileMappingA GetModuleFileNameA GetModuleHandleA
make_import_lib shell32 SHELL32.dll ShellExecuteA
make_import_lib advapi32 ADVAPI32.dll SetEntriesInAclA InitializeSecurityDescriptor SetNamedSecurityInfoW SetSecurityDescriptorDacl InitializeAcl AddAce GetAclInformation MakeAbsoluteSD
make_import_lib mfc42 MFC42.dll AfxWinMain AfxEnableControlContainer AfxSocketInit

"$clang_bin" --target=x86_64-pc-windows-msvc -c "$fixture_dir/control.c" \
  -o "$build_dir/control.obj" -O0
"$rc_bin" /fo "$build_dir/positive.res" "$fixture_dir/positive.rc"
"$link_bin" /nologo /nodefaultlib /subsystem:console /debug:full \
  /entry:mainCRTStartup /out:"$build_dir/positive.exe" \
  /pdb:"$build_dir/LPADV.pdb" /pdbaltpath:LPADV.pdb \
  "$build_dir/control.obj" "$build_dir/positive.res" \
  "$build_dir/kernel32.lib" "$build_dir/shell32.lib" \
  "$build_dir/advapi32.lib" "$build_dir/mfc42.lib"

python3 - "$build_dir/positive.exe" "$fixture_dir" <<'PY'
import sys
from pathlib import Path

source = Path(sys.argv[1]).read_bytes()
destination = Path(sys.argv[2])
variants = {
    "positive-all-profiles.exe": source,
    "near-miss-service-host-pdb.exe": (b"LPADV.pdb", b"OTHER.pdb"),
    "near-miss-browser-cshare.exe": (b"CShareMemory_", b"XShareMemory_"),
    "near-miss-browser-handler.exe": (
        b"function fnOnError(msg,url,lineno){return true;}window.onerror=fnOnError;",
        b"function fnOnError(msg,url,lineno){return fals;}window.onerror=fnOnError;",
    ),
}
for filename, value in variants.items():
    if isinstance(value, tuple):
        old, new = value
        assert len(old) == len(new) and source.count(old) == 1, (filename, old)
        value = source.replace(old, new, 1)
    (destination / filename).write_bytes(value)
PY
