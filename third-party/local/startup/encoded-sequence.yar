rule Encoded_Autorun_Sequence
{
    meta:
        description = "Encoded carrier implements an autorun persistence sequence"
        scan_context = "file"

    strings:
        $mz = /TVqQAA[A-Za-z0-9+\/]{30,}/ ascii
        $dos = /VGhpcy[A-Za-z0-9+\/]wcm9ncmFtIGNhbm5vdCBiZSBydW4gaW4gRE9TIG1vZGU/ ascii
        $clr1 = "X0NvckV4ZU1haW" ascii
        $clr2 = "X0NvckRsbE1haW" ascii
        $clr3 = "9Db3JEbGxNYWlu" ascii
        $wscript1 = "VwBTAGMAcgBpAHAAdA" ascii
        $wscript2 = "cAUwBjAHIAaQBwAHQA" ascii
        $wscript3 = "XAFMAYwByAGkAcAB0A" ascii
        $folders = "UwBwAGUAYwBpAGEAbABGAG8AbABkAGUAcgBzAA" ascii
        $startup = "UwB0AGEAcgB0AHUAcAA" ascii
        $shortcut = "UMAcgBlAGEAdABlAFMAaABvAHIAdABjAHUAdAA" ascii
        $powershell = "UABvAHcAZQByAFMAaABlAGwAbA" ascii

    condition:
        filesize >= 4096 and filesize <= 10485760 and $mz at 0 and $dos and
        1 of ($clr*) and 1 of ($wscript*) and $folders and $startup and
        $shortcut and $powershell
}
