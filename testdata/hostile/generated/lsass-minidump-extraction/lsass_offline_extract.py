"""Offline LSASS minidump credential extraction (positive control)."""
import struct

DUMP_PATH = "lsass.dmp"


def extract_credentials_from_minidump(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if data[0:4] != b"MDMP":
        raise ValueError("not a minidump")
    return [{"msv": {"nt_hash": b"\x00" * 16}}]


def main():
    creds = extract_credentials_from_minidump(DUMP_PATH)
    expected_nt = "bbf7d1528afa8b0fdd40a5b2531bbb6d"
    for entry in creds:
        nt_hash = entry["msv"]["nt_hash"].hex()
        if nt_hash == expected_nt:
            print("match:", nt_hash)


if __name__ == "__main__":
    main()
