VERSION 5.00
Attribute VB_Name = "Form1"
Private Sub Command1_Click()
    Dim buf1 As String * 2
    Dim samp_text As String
    samp_text = "Hello"
    Dim i As Long
    For i = 0 To Len(samp_text)
        CopyMemory ByVal buf1, VarPtr(samp_text) + i, 1
        Print buf1
    Next i
End Sub
