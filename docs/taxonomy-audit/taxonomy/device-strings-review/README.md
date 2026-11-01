# Legacy device-string review

The retired `metadata/file/string/device` leaf mixed unrelated text observations. Industrial-control acronyms and a turbine-speed identifier now live in industrial vocabulary; their co-occurrence is an industrial-control profile, not proof of an operation. Generic words and reboot vocabulary have neutral lexical homes, and the USB VID/PID pattern is a device identifier. VirtualBox registry and SDK references live with that product.

The two VirtualBox observations changed from baseline to notable to meet the identity policy for `well-known/`. Their nonempty text matchers also imply the one-byte minimum added to meet the existing size policy. Other matchers, scopes and criticalities are preserved.

The adjacent crowded content-word leaf also contained physical-process vocabulary and uppercase action words. Those moved into physical and action vocabulary siblings; their observations still do not imply a device action. Exact consumers were updated.
