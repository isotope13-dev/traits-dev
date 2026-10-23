Set host = CreateObject("WScript.Shell")
deadline = DateAdd("s", 2, Now())
Do Until Now() > deadline
  WScript.Sleep 100
Loop
fragment = "E"
Execute "host." + fragment + "xec(""cmd /c echo decoded-stage"")"
