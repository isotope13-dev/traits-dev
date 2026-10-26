#!/usr/bin/env python3
"""Build minimal, harmless zip-based package artifacts.

Each kind produces a single archive whose only payload is a benign text
message plus the real does-nothing binary when the format calls for one
(APK native lib, AAR classes.jar, IPA app executable). The per-format
metadata files (manifests, plists, specs, etc.) are just enough to be
recognized as that format by type detectors.
"""

from __future__ import annotations

import io
import lzma
import sys
import zipfile
from pathlib import Path

MESSAGE = "this sample does nothing"

JAR_MANIFEST = """Manifest-Version: 1.0
Created-By: sample
Main-Class: Sample

"""

WAR_WEB_XML = """<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="https://jakarta.ee/xml/ns/jakartaee" version="5.0">
  <display-name>Sample</display-name>
</web-app>
"""

EAR_APPLICATION_XML = """<?xml version="1.0" encoding="UTF-8"?>
<application xmlns="https://jakarta.ee/xml/ns/jakartaee" version="9">
  <display-name>Sample</display-name>
  <module><web><web-uri>sample.war</web-uri><context-root>/sample</context-root></web></module>
</application>
"""

ANDROID_MANIFEST = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.sample"
    android:versionCode="1"
    android:versionName="1.0">
  <application android:label="Sample"/>
</manifest>
"""

AAR_PROGUARD = "# sample aar, no rules\n"

APK_STRINGS = """<?xml version="1.0" encoding="utf-8"?>
<resources>
  <string name="message">this sample does nothing</string>
</resources>
"""

IPA_INFO_PLIST = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleIdentifier</key><string>com.example.sample</string>
  <key>CFBundleName</key><string>Sample</string>
  <key>CFBundleExecutable</key><string>Sample</string>
  <key>CFBundleVersion</key><string>1</string>
  <key>CFBundleShortVersionString</key><string>1.0</string>
</dict>
</plist>
"""

XPI_MANIFEST = """{
  "manifest_version": 2,
  "name": "Sample",
  "version": "1.0",
  "description": "A sample extension that does nothing.",
  "browser_specific_settings": {
    "gecko": { "id": "sample@example.com" }
  }
}
"""

EPUB_CONTAINER = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

EPUB_CONTENT_OPF = """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="book-id" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">sample</dc:identifier>
    <dc:title>Sample</dc:title>
    <dc:language>en</dc:language>
  </metadata>
  <manifest>
    <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine><itemref idref="chapter1"/></spine>
</package>
"""

EPUB_CHAPTER = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head><title>Sample</title></head>
  <body><p>this sample does nothing</p></body>
</html>
"""

NUSPEC = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd">
  <metadata>
    <id>Sample</id>
    <version>1.0.0</version>
    <authors>example</authors>
    <description>A sample package that does nothing.</description>
  </metadata>
</package>
"""

VSIX_MANIFEST = """<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011">
  <Metadata>
    <Identity Language="en-US" Id="Sample" Version="1.0.0" Publisher="example"/>
    <DisplayName>Sample</DisplayName>
    <Description>A sample extension that does nothing.</Description>
  </Metadata>
  <Installation><InstallationTarget Id="Microsoft.VisualStudio.Community"/></Installation>
</PackageManifest>
"""

VSIX_CONTENT_TYPES = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="vsixmanifest" ContentType="text/xml"/>
  <Default Extension="txt" ContentType="text/plain"/>
</Types>
"""

WHEEL_METADATA = """Metadata-Version: 2.1
Name: sample
Version: 0.1.0
Summary: A sample package that does nothing.
License: MIT
"""

WHEEL_WHEEL = """Wheel-Version: 1.0
Generator: sample 0.1.0
Root-Is-Purelib: true
Tag: py3-none-any
"""

WHEEL_RECORD = "sample/__init__.py,,\nsample-0.1.0.dist-info/METADATA,,\nsample-0.1.0.dist-info/WHEEL,,\nsample-0.1.0.dist-info/RECORD,,\n"

EGG_PKG_INFO = """Metadata-Version: 2.1
Name: sample
Version: 0.1.0
Summary: A sample egg that does nothing.
"""

CONDA_METADATA = """{
  "conda_pkg_format_version": 2,
  "package_metadata_version": 1
}
"""

CONDA_INDEX = """{
  "name": "sample",
  "version": "0.1.0",
  "build": "0",
  "build_number": 0,
  "subdir": "noarch",
  "depends": [],
  "license": "MIT"
}
"""


def write(z: zipfile.ZipFile, name: str, data: str) -> None:
    z.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)


def load_xz(path: Path) -> bytes:
    with lzma.open(path) as f:
        return f.read()


def build_jar(z: zipfile.ZipFile) -> None:
    write(z, "META-INF/MANIFEST.MF", JAR_MANIFEST)
    write(z, "Sample.txt", MESSAGE + "\n")


def build_war(z: zipfile.ZipFile) -> None:
    write(z, "META-INF/MANIFEST.MF", JAR_MANIFEST)
    write(z, "WEB-INF/web.xml", WAR_WEB_XML)
    write(z, "index.txt", MESSAGE + "\n")


def build_ear(z: zipfile.ZipFile) -> None:
    write(z, "META-INF/MANIFEST.MF", JAR_MANIFEST)
    write(z, "META-INF/application.xml", EAR_APPLICATION_XML)


def build_apk(z: zipfile.ZipFile, linux_xz: Path) -> None:
    write(z, "AndroidManifest.xml", ANDROID_MANIFEST)
    write(z, "META-INF/MANIFEST.MF", JAR_MANIFEST)
    write(z, "res/values/strings.xml", APK_STRINGS)
    z.writestr("lib/x86/libsample.so", load_xz(linux_xz), zipfile.ZIP_DEFLATED)


def build_aar(z: zipfile.ZipFile, class_file: Path) -> None:
    write(z, "AndroidManifest.xml", ANDROID_MANIFEST)
    write(z, "R.txt", "")
    write(z, "proguard.txt", AAR_PROGUARD)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as inner:
        inner.writestr("META-INF/MANIFEST.MF", JAR_MANIFEST)
        inner.writestr("Sample.class", class_file.read_bytes())
    z.writestr("classes.jar", buf.getvalue(), zipfile.ZIP_DEFLATED)


def build_ipa(z: zipfile.ZipFile, darwin_xz: Path) -> None:
    write(z, "Payload/Sample.app/Info.plist", IPA_INFO_PLIST)
    z.writestr("Payload/Sample.app/Sample", load_xz(darwin_xz), zipfile.ZIP_DEFLATED)


def build_xpi(z: zipfile.ZipFile) -> None:
    write(z, "manifest.json", XPI_MANIFEST)


def build_epub(z: zipfile.ZipFile) -> None:
    info = zipfile.ZipInfo("mimetype")
    info.compress_type = zipfile.ZIP_STORED
    z.writestr(info, "application/epub+zip")
    write(z, "META-INF/container.xml", EPUB_CONTAINER)
    write(z, "OEBPS/content.opf", EPUB_CONTENT_OPF)
    write(z, "OEBPS/chapter1.xhtml", EPUB_CHAPTER)


def build_nupkg(z: zipfile.ZipFile) -> None:
    write(z, "Sample.nuspec", NUSPEC)
    write(z, "content/readme.txt", MESSAGE + "\n")


def build_vsix(z: zipfile.ZipFile) -> None:
    write(z, "extension.vsixmanifest", VSIX_MANIFEST)
    write(z, "[Content_Types].xml", VSIX_CONTENT_TYPES)
    write(z, "extension/readme.txt", MESSAGE + "\n")


def build_whl(z: zipfile.ZipFile) -> None:
    write(z, "sample/__init__.py", f'"""Sample package."""\nMESSAGE = "{MESSAGE}"\n')
    write(z, "sample-0.1.0.dist-info/METADATA", WHEEL_METADATA)
    write(z, "sample-0.1.0.dist-info/WHEEL", WHEEL_WHEEL)
    write(z, "sample-0.1.0.dist-info/RECORD", WHEEL_RECORD)


def build_egg(z: zipfile.ZipFile) -> None:
    write(z, "sample/__init__.py", f'"""Sample egg."""\nMESSAGE = "{MESSAGE}"\n')
    write(z, "EGG-INFO/PKG-INFO", EGG_PKG_INFO)


def build_conda(z: zipfile.ZipFile) -> None:
    write(z, "metadata.json", CONDA_METADATA)
    write(z, "info/index.json", CONDA_INDEX)
    write(z, "info/files", "share/doc/sample/README\n")
    write(z, "pkg/share/doc/sample/README", MESSAGE + "\n")


def main(kind: str, target: Path, *extras: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        if kind == "apk":
            build_apk(z, Path(extras[0]))
        elif kind == "aar":
            build_aar(z, Path(extras[0]))
        elif kind == "ipa":
            build_ipa(z, Path(extras[0]))
        elif kind == "jar":
            build_jar(z)
        elif kind == "war":
            build_war(z)
        elif kind == "ear":
            build_ear(z)
        elif kind == "xpi":
            build_xpi(z)
        elif kind == "epub":
            build_epub(z)
        elif kind == "nupkg":
            build_nupkg(z)
        elif kind == "vsix":
            build_vsix(z)
        elif kind == "whl":
            build_whl(z)
        elif kind == "egg":
            build_egg(z)
        elif kind == "conda":
            build_conda(z)
        else:
            raise SystemExit(f"unknown kind: {kind}")


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]), *sys.argv[3:])
