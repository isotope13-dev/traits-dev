#!/usr/bin/env python3
"""Generate a minimal OpenDocument file (.odt, .ods, or .odp)."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

MIMETYPES = {
    "odt": "application/vnd.oasis.opendocument.text",
    "ods": "application/vnd.oasis.opendocument.spreadsheet",
    "odp": "application/vnd.oasis.opendocument.presentation",
}

MANIFEST_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">
  <manifest:file-entry manifest:full-path="/" manifest:version="1.2" manifest:media-type="{mimetype}"/>
  <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
</manifest:manifest>
"""

CONTENT_ODT = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    office:version="1.2">
  <office:body>
    <office:text>
      <text:p>this sample does nothing</text:p>
    </office:text>
  </office:body>
</office:document-content>
"""

CONTENT_ODS = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    office:version="1.2">
  <office:body>
    <office:spreadsheet>
      <table:table table:name="Sheet1">
        <table:table-row>
          <table:table-cell office:value-type="string">
            <text:p>this sample does nothing</text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>
    </office:spreadsheet>
  </office:body>
</office:document-content>
"""

CONTENT_ODP = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    office:version="1.2">
  <office:body>
    <office:presentation>
      <draw:page draw:name="slide1">
        <draw:frame>
          <draw:text-box>
            <text:p>this sample does nothing</text:p>
          </draw:text-box>
        </draw:frame>
      </draw:page>
    </office:presentation>
  </office:body>
</office:document-content>
"""

CONTENTS = {"odt": CONTENT_ODT, "ods": CONTENT_ODS, "odp": CONTENT_ODP}


def main(kind: str, target: Path) -> None:
    if kind not in MIMETYPES:
        raise SystemExit(f"unknown kind: {kind}")
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w") as z:
        # mimetype must be first and stored uncompressed per the ODF spec.
        info = zipfile.ZipInfo("mimetype")
        info.compress_type = zipfile.ZIP_STORED
        z.writestr(info, MIMETYPES[kind])
        z.writestr("META-INF/manifest.xml", MANIFEST_TEMPLATE.format(mimetype=MIMETYPES[kind]), zipfile.ZIP_DEFLATED)
        z.writestr("content.xml", CONTENTS[kind], zipfile.ZIP_DEFLATED)


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]))
