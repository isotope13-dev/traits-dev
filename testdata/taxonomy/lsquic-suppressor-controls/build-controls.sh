#!/bin/sh
set -eu
cd "$(dirname "$0")"
cc -shared -fPIC -Wl,--build-id=none decoy-lsquic-stub.c -o libdecoylsquic.so
cc -O0 -fno-pie -no-pie -Wl,--build-id=none -DWITH_SOCKET packet-flood-control.c -o packets-and-socket-no-symbol
cc -O0 -fno-pie -no-pie -Wl,--build-id=none -DWITH_LSQUIC_IMPORT packet-flood-control.c -L. -Wl,-rpath,'$ORIGIN' -ldecoylsquic -o packets-with-copied-symbol
cc -O0 -fno-pie -no-pie -Wl,--build-id=none -DWITH_SOCKET -DWITH_TARGET_USAGE packet-flood-control.c -o packets-targeted-socket-no-symbol
cc -O0 -fno-pie -no-pie -Wl,--build-id=none -DWITH_SOCKET -DWITH_TARGET_USAGE -DWITH_LSQUIC_IMPORT packet-flood-control.c -L. -Wl,-rpath,'$ORIGIN' -ldecoylsquic -o packets-and-socket-with-copied-symbol
cp packets-and-socket-no-symbol sibling-behavior/packets-and-socket
cp packets-with-copied-symbol sibling-behavior/sibling-symbol-only
