<job id="fixture">
<script language="VBScript">
' Numeric-table execute-loader fixture: the delimiter is sliced out of a
' carrier with Mid, a numeric table splits on it, cells decode through
' Chr division, and the rebuilt stage feeds Execute.
overpower = overpower + ("zz\qqyes")
blob = blob + ("\qq4104\qq3939\qq3774\qq3839")
key = mid(overpower,7,4)
cells = Split(blob,key,-1,0)
for i = 1 to Ubound(cells)
  stage = stage & chr(Clng(cells(i)) / 57)
Next
execute cstr(stage)+cstr(extra)
</script>
</job>
