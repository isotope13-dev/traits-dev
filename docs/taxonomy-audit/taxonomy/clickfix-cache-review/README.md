# Browser-cache delivery review

The former ClickFix browser-cache category grouped generic operations with script launch and clipboard-assisted delivery. The rules now follow their evidence:

- Configured image-request clues are script network profiles; the `steg` text match does not by itself prove a steganographic payload.
- Findstr output redirection, Certutil decoding, and browser profile/cache paths live with their respective operations and path subjects.
- Cache carving and temporary script-host execution live under the browser-cache execution sink. Firefox-profile entry copying and size-selected profile copying live under a separate browser-profile execution sink: those conditions do not themselves establish a cache directory.
- Clipboard-write combinations live under the clipboard execution lure, without claiming that all independently matched operations share a data flow.

The browser-cache legacy leaf is removed, and its consumers have been updated. Other ClickFix branches remain to be reviewed.
