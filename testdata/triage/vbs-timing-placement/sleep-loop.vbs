deadline = DateAdd("s", 2, Now())
Do Until Now() > deadline
  WScript.Sleep 100
Loop
