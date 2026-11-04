# Shellcode filetype mislabeled-bad review — 2026-11-04

All four samples are bad. Their original scanner runs produced no hostile findings; the additions below combine the observable code or payload facts without adding engine features.

`e1c958bf9d78` begins with a repeating-key XOR decoder. Static decoding recovers a Windows x64 DLL; neither scanner identified a hostile behavior in the carved DLL, so the classification rests on the large self-decoding executable stage and its hostile obfuscation, not an asserted DLL payload function. `e9ba441b81f2` begins with a fixed-XOR in-place decoder over an approximately 1.8 MB stage. Static decoding exposes multiple PE images; scans of carved tails find RAT and rootkit characteristics, but those tails overlap multiple images, so the individual attribution is not established. Both original files match the new large XOR-decoder finding in both scanners. Changing the XOR instruction clears their controls.

`d26158822bc5` contains an embedded Windows DLL with commands that remove Telegram session and browser data, clear browser tracks, and force-kill administration tools. A new finding combines the Telegram deletion and two admin-tool kill commands. Both scanners match the original shellcode and carved PE; changing the registry-editor kill target clears the control. The finding combines file-level command facts rather than proving their execution order.

`ef095e5c8e55` contains a Windows DLL with keyboard-hook and clipboard collection, a command disabling UAC, and additional RAT behavior. Existing findings identify these behaviors in the carved PE; expanding existing facts to shellcode and combining them now identifies the original in both scanners. Changing the UAC value name clears the control. The combined facts do not establish that all capabilities execute in a particular run.

Full validation passed after the changes.
