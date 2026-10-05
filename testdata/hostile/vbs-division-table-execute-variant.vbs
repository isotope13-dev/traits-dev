<job id="variant">
<script language="VBScript">
' Division-table loader variant: different carrier names, no "power"
' token anywhere, divisor 41. Must still convict both hostile loaders
' through the technique matchers, not sample-specific strings.
carrier = carrier + ("ab##cd")
blob = blob + ("##2706##2542##2419##2501")
sep = Mid(carrier,5,2)
parts = Split(blob,sep,-1,0)
For j = 1 To UBound(parts)
  stage = stage & Chr(Clng(parts(j)) / 41)
Next
Execute CStr(stage)
</script>
</job>
