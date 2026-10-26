# Legitimate uninstall policy with CJK documentation: plain-ASCII msiexec
# switches plus fullwidth punctuation in the comment. The confusable-letter
# atom must stay silent here -- CJK text is not a homoglyph switch.
# MSI 单独走 msiexec 重构(最稳、最静默)。
$guid = '{12345678-1234-1234-1234-123456789ABC}'
msiexec /x $guid /qn /norestart
