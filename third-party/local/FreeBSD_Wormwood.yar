rule FreeBSD_Wormwood_Companion_Virus
{
    meta:
        description = "Detects FreeBSD.Wormwood companion virus assembly source code"
        author = "cleave-rules"
        date = "2026-03-21"
        family = "Wormwood"
        platform = "FreeBSD"
        category = "virus"

    strings:
        $name = "[FreeBSD.Wormwood]" ascii
        $revelation = "REV.8:11 The name of the star is Wormwood" ascii
        $virusstart = "_VirusStart:" ascii
        $processfile = "_ProcessFile:" ascii
        $virus_size = "VIRUS_SIZE" ascii

    condition:
        filesize < 100KB and 3 of them
}
