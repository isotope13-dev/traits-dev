#!/bin/sh
# Rebuild inert JVM controls; this compiles them without executing any class.
set -eu
fixture_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
fixture_build_dir=$(mktemp -d /tmp/jvm-abi-controls.XXXXXX)
"${JAVAC:-javac}" -d "$fixture_build_dir" "$fixture_dir"/src/*.java
for fixture_name in AbiReaderControl MaskedBinaryControl Pbkdf2ReferenceOnly RawPostControl; do
  cp "$fixture_build_dir/$fixture_name.class" "$fixture_dir/../benign/"
done
cp "$fixture_build_dir/MaskedStringControl.class" "$fixture_dir/controls/"
cp "$fixture_build_dir/ObfuscatedAbiNoAccount.class" "$fixture_dir/controls/"
python3 - "$fixture_build_dir" "$fixture_dir/controls/jvm-split-abi-and-xor-control.jar" <<'PY'
import pathlib,sys,zipfile
root=pathlib.Path(sys.argv[1])
with zipfile.ZipFile(sys.argv[2],'w',zipfile.ZIP_DEFLATED) as z:
 for name in ['AbiReaderControl.class','MaskedStringControl.class','RawPostControl.class']:
  info=zipfile.ZipInfo(name, date_time=(1980,1,1,0,0,0))
  info.compress_type=zipfile.ZIP_DEFLATED
  z.writestr(info,(root/name).read_bytes())
PY
