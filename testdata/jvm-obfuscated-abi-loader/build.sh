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

# Derive the source-role near miss from the byte-preserving hostile fixture.
python3 - "$fixture_dir/../hostile/jvm-native-browser-collector.jar" "$fixture_dir/controls/jvm-secret-apis-no-browser-source.jar" <<'PYCODE'
import sys,zipfile
with zipfile.ZipFile(sys.argv[1]) as source, zipfile.ZipFile(sys.argv[2], 'w', zipfile.ZIP_DEFLATED) as output:
 for member in source.infolist():
  if member.filename != 'com/example/handlers/browser/PasswordHandler.class':
   output.writestr(member, source.read(member.filename))
PYCODE
