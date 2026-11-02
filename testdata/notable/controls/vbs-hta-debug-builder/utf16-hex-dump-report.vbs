' Benign UTF-16 word hex dump utility using OpenAsTextStream(1, -1) and Hex(AscW).
Option Explicit
Dim fs, f, reader, report, idx, wordHex

Set fs = CreateObject("Scripting.FileSystemObject")
Set f = fs.GetFile(WScript.Arguments(0))
Set reader = f.OpenAsTextStream(1, -1)
Set report = fs.CreateTextFile(WScript.Arguments(1), True)

idx = 0
Do While Not reader.AtEndOfStream
    wordHex = Right("0000" & Hex(AscW(reader.Read(1))), 4)
    report.WriteLine Right("000000" & Hex(idx * 2), 6) & ": " & wordHex
    idx = idx + 1
Loop

reader.Close
report.Close
