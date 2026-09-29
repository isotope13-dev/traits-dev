#!/usr/bin/env python3
"""Cover direct WhatsApp chat-store enumeration in messaging objectives."""

from pathlib import Path
import json
import subprocess
import tempfile
import zipfile


AUTOMATION_RULE = (
    "objectives/lateral-movement/social-engineering/spam::"
    "extension-injects-messaging-account-automation"
)
EXPORT_RULE = (
    "objectives/lateral-movement/social-engineering/spam::"
    "extension-exports-messaging-contact-list"
)


def make_extension(path: Path, matches: list[str], source: str) -> None:
    manifest = json.dumps(
        {
            "manifest_version": 3,
            "content_scripts": [{"matches": matches, "js": ["content.js"]}],
        }
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("manifest.json", manifest)
        archive.writestr("content.js", source)


def check(cleave: str, traits: Path, path: Path, rule: str, expected: bool) -> None:
    result = subprocess.run(
        [cleave, "--traits-dir", str(traits), "test-rules", "--rules", rule, str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    output = result.stdout + result.stderr
    marker = ("MATCHED " if expected else "NOT MATCHED ") + rule + " (composite) "
    if not any(line.startswith(marker) for line in output.splitlines()):
        raise AssertionError(f"{path.name}: expected {marker.strip()}\n{output}")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    cleave = str(root.parent / "cleave/target/release/cleave")
    whatsapp = ["https://web.whatsapp.com/*"]
    direct_chat_enumeration = """
      const recipients = [];
      for (const chat of WPP.whatsapp.ChatStore._models) {
        if (chat.id.server.startsWith("c")) {
          recipients.push({number: chat.id.user, name: chat.name});
        }
      }
      WPP.chat.sendTextMessage(chatId, message);
    """
    contact_export = direct_chat_enumeration + """
      const anchor = document.createElement("a");
      anchor.href = URL.createObjectURL(new Blob([csv], {type: "text/csv"}));
      anchor.download = "contacts.csv";
      anchor.click();
    """

    with tempfile.TemporaryDirectory(prefix="whatsapp-web-automation-") as directory:
        temp = Path(directory)

        positive = temp / "crm-chat-export.zip"
        make_extension(positive, whatsapp, contact_export)
        check(cleave, root, positive, AUTOMATION_RULE, True)
        check(cleave, root, positive, EXPORT_RULE, True)

        no_send = temp / "chat-export-only.zip"
        make_extension(
            no_send,
            whatsapp,
            contact_export.replace("WPP.chat.sendTextMessage(chatId, message);", ""),
        )
        check(cleave, root, no_send, AUTOMATION_RULE, False)
        check(cleave, root, no_send, EXPORT_RULE, True)

        no_messaging_host = temp / "unscoped-chat-export.zip"
        make_extension(no_messaging_host, ["https://example.com/*"], contact_export)
        check(cleave, root, no_messaging_host, AUTOMATION_RULE, False)
        check(cleave, root, no_messaging_host, EXPORT_RULE, False)

        store_reference_without_iteration = temp / "store-reference-only.zip"
        make_extension(
            store_reference_without_iteration,
            whatsapp,
            "const chats = WPP.whatsapp.ChatStore._models; "
            "WPP.chat.sendTextMessage(chatId, message);",
        )
        check(cleave, root, store_reference_without_iteration, AUTOMATION_RULE, False)
        check(cleave, root, store_reference_without_iteration, EXPORT_RULE, False)

        send_without_enumeration = temp / "single-chat-send.zip"
        make_extension(
            send_without_enumeration,
            whatsapp,
            "WPP.chat.sendTextMessage(chatId, message);",
        )
        check(cleave, root, send_without_enumeration, AUTOMATION_RULE, False)
        check(cleave, root, send_without_enumeration, EXPORT_RULE, False)

    print("PASS WhatsApp automation needs chat enumeration plus send; contact export needs CSV output")


if __name__ == "__main__":
    main()
