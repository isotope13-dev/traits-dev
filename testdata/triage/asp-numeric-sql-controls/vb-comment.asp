<%
' Execute(unpackCells("%98%136%124%87%132%141%53%55%122%141%118%130%133%129%122%55"))

Function unpackCells(cells)
  cells = Split(cells,"%")
  For j=1 To UBound(cells)
    unpackCells=unpackCells & Chr(cells(j)-21)
  Next
End Function
%>
