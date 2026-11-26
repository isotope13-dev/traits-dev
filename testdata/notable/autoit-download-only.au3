Func FETCHNOTE()
  InetGet ( "https://example.com/notes.txt" , @TempDir & "\notes.txt" , 1 )
  Return 0
EndFunc
