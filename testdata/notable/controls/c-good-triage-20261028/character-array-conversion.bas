For xx = 0 To Len(szpassword) - 1
 p.ch(xx) = Asc(Mid(szpassword, xx + 1, 1))
Next
p.ch(xx) = Chr(0)
