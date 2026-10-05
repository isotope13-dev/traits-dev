<job id="controls">
<script language="VBScript">
' Benign Mid/Split control: the Mid slice formats a display label while a
' nearby Split parses on a literal comma. No variable delimiter means the
' Mid-sliced-delimiter composite must stay silent here.
label = Mid(reportTitle,1,12)
fields = Split(csvLine,",",-1,0)
For k = 0 To UBound(fields)
  total = total & fields(k)
Next
</script>
</job>
