rule MintsLoader {
    meta:
        author = "RussianPanda"
        description = "Detects MintsLoader scripts"
        date = "01/16/2026"
    
    strings:
        $s1 = "Get-Date).DayOfYear" ascii wide nocase
        $s2 = ".php?id=$" ascii wide nocase
        $s3 = ".top" ascii wide
        $s4 = "$global" ascii wide
        
    condition:
        $s1 and 2 of ($s2, $s3, $s4)
}
