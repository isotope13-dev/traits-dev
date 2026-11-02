#!/usr/bin/env python3
"""Check Swift capture, clipboard, local model, and MCP observations statically."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="../cleave/target/release/cleave")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    screen = "micro-behaviors/hardware/display/screen::swift-screencapturekit-stream-create"
    displays = "micro-behaviors/hardware/display/screen::swift-shareable-display-content-query"
    media = "micro-behaviors/hardware/input/media::swift-avfoundation-capture-session-create"
    permission = "micro-behaviors/hardware/input/media::swift-media-permission-request"
    authorization = "micro-behaviors/hardware/input/media::swift-media-permission-check"
    clipboard = "micro-behaviors/os/clipboard/reference::swift-general-pasteboard-reference"
    counter = "micro-behaviors/os/clipboard/monitor::swift-pasteboard-change-count-read"
    read = "micro-behaviors/os/clipboard/read::swift-general-pasteboard-content-read"
    model = "micro-behaviors/data/llm/session::swift-foundation-model-session-create"
    mcp = "micro-behaviors/communications/ipc/mcp::"
    capture = "metadata/lang/source/naming/flag::body-capture-enabled-setting"
    # Each tuple gives inert source, required observations, and forbidden claims.
    # Permission checks, enumeration and counter reads do not prove content capture.
    cases = {
        "stream.swift": ('let stream = SCStream(filter: filter, configuration: config, delegate: nil)\n', {screen}, set()),
        "qualified-stream.swift": ('let stream = ScreenCaptureKit.SCStream(filter: filter, configuration: config, delegate: nil)\n', {screen}, set()),
        "stream-reference.swift": ('let name = "SCStream(filter: filter, configuration: config)"\n// SCStream(filter: filter)\n', set(), {screen}),
        "displays.swift": ('SCShareableContent.getExcludingDesktopWindows(false, onScreenWindowsOnly: true) { content, error in }\n', {displays}, {screen}),
        "permission.swift": ('AVCaptureDevice.requestAccess(for: .audio) { allowed in }\n', {permission}, {screen, media}),
        "authorization.swift": ('let status = AVCaptureDevice.authorizationStatus(for: .video)\n', {authorization}, {screen, media}),
        "permission-reference.swift": ('let help = "AVCaptureDevice.requestAccess(for: .audio)"\n', set(), {permission, authorization}),
        "capture-session.swift": ('let session = AVCaptureSession()\n', {media}, set()),
        "clipboard-counter.swift": ('let changeCount = NSPasteboard.general.changeCount\n', {clipboard, counter}, {read}),
        "clipboard-read.swift": ('let text = NSPasteboard.general.string(forType: .string)\n', {read}, set()),
        "clipboard-data.swift": ('let data = NSPasteboard.general.data(forType: .png)\n', {read}, set()),
        "clipboard-reference.swift": ('let board = NSPasteboard.general\n', {clipboard}, {read, counter}),
        "clipboard-type.swift": ('func inspect(_ pasteboard: NSPasteboard) {}\n', set(), {clipboard, read, counter}),
        "other-properties.swift": ('let count = state.changeCount\nlet value = decoder.string(forType: .string)\n', set(), {clipboard, read, counter}),
        "clipboard-comment.swift": ('// let data = NSPasteboard.general.data(forType: .png)\nlet help = "NSPasteboard.general.changeCount"\n', set(), {clipboard, read, counter}),
        "foundation-model.swift": ('let session = LanguageModelSession(instructions: "Summarize this note")\n', {model}, set()),
        "qualified-model.swift": ('let session = FoundationModels.LanguageModelSession()\n', {model}, set()),
        "model-reference.swift": ('let help = "LanguageModelSession()"\n// LanguageModelSession()\n', set(), {model}),
        "mcp-client.swift": ('let methods = ["tools/call", "tools/list"]\nlet result = ["protocolVersion": "2024-11-05", "serverInfo": "local"]\n',
                             {mcp + "mcp-tools-call-method", mcp + "mcp-tools-list-method", mcp + "mcp-initialize-result", mcp + "mcp-tool-method-version-references"}, set()),
        "mcp-resource-client.swift": ('let methods = ["resources/list", "resources/read"]\n',
                                     {mcp + "mcp-resource-method-references"}, {mcp + "mcp-resource-authentication-references"}),
        "mcp-lookalikes.swift": ('let names = ["tools/call_extra", "tools/listing", "https://example.test/tools/list", "resources/reader", "resources/listing"]\n',
                                set(), {mcp + name for name in ["mcp-tools-call-method", "mcp-tools-list-method", "mcp-resources-list-method", "mcp-resources-read-method"]}),
        "resources.js": ('const methods = ["resources/list", "resources/read"];\n',
                         {mcp + "mcp-resource-method-references"}, {mcp + "mcp-resource-authentication-references"}),
        "disabled-benchmark.py": ('benchmark = "request_body_capture_disabled"\n', set(), {capture}),
        "enabled.py": ('body_capture = True\n', {capture}, set()),
        "disabled.py": ('body_capture = False\n', set(), {capture}),
    }
    with tempfile.TemporaryDirectory(prefix="swift-archive-improve-") as directory:
        work = Path(directory)
        for name, (source, _, _) in cases.items():
            (work / name).write_text(source)
        result = subprocess.run(
            [str((repo / args.cleave).resolve()), "--traits-dir", str(repo), "--all-files",
             "--format", "json", str(work)], check=True, text=True, capture_output=True,
        )
        reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        files = {Path(f["path"]).name: f for report in reports for f in report["files"]}
        for name, (_, required, forbidden) in cases.items():
            traits = files[name].get("traits", [])
            ids = {t["id"] for t in traits}
            assert required <= ids, (name, "missing", required - ids)
            assert not forbidden & ids, (name, "forbidden", forbidden & ids)
            elevated = [t["id"] for t in traits if t["crit"] >= 4]
            assert not elevated, (name, "elevated", elevated)
            print(f"PASS {name}")
    print(f"{len(cases)} Swift archive improvement controls passed")


if __name__ == "__main__":
    main()
