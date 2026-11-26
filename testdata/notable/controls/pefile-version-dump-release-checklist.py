#!/usr/bin/env python3
"""Print the StringFileInfo version strings of a PE file (release checklist)."""
import sys

import pefile


def main():
    pe = pefile.PE(sys.argv[1], fast_load=True)
    pe.parse_data_directories(
        directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_RESOURCE"]])
    for group in getattr(pe, "FileInfo", []) or []:
        for entry in group:
            if entry.name == "StringFileInfo":
                for table in entry.StringTable:
                    for key, val in table.entries.items():
                        print(key.decode("latin-1"), val.decode("latin-1"))


if __name__ == "__main__":
    main()
