' Locale-aware message formatter: builds labels from character codes so a
' single script serves every code page without string literals.
Dim sep, lblOk, lblCancel, i
sep = Chr(44)
lblOk = Chr(79) & Chr(75)
lblCancel = Chr(67) & Chr(97) & Chr(110) & Chr(99) & Chr(101) & Chr(108)
WScript.Echo lblOk & sep & lblCancel
