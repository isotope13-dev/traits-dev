rule Encoded_Download_Decode_Invoke
{
    meta:
        description = "Encoded carrier downloads, decodes, and reflectively loads code"
        scan_context = "file"

    strings:
        $mz = /TVqQAA[A-Za-z0-9+\/]{30,}/ ascii
        $dos = /VGhpcy[A-Za-z0-9+\/]wcm9ncmFtIGNhbm5vdCBiZSBydW4gaW4gRE9TIG1vZGU/ ascii
        $clr1 = "X0NvckV4ZU1haW" ascii
        $clr2 = "X0NvckRsbE1haW" ascii
        $clr3 = "9Db3JEbGxNYWlu" ascii
        $download1 = "RG93bmxvYWRTdHJpbm" ascii
        $download2 = "Rvd25sb2FkU3RyaW5n" ascii
        $download3 = "Eb3dubG9hZFN0cmluZ" ascii
        $decode1 = "RnJvbUJhc2U2NFN0cmluZ" ascii
        $decode2 = "Zyb21CYXNlNjRTdHJpbm" ascii
        $decode3 = "Gcm9tQmFzZTY0U3RyaW5n" ascii
        $reflect1 = "R2V0TWV0aG9k" ascii
        $reflect2 = "dldE1ldGhvZ" ascii
        $reflect3 = "HZXRNZXRob2" ascii

    condition:
        filesize >= 4096 and filesize <= 10485760 and $mz at 0 and $dos and
        1 of ($clr*) and 1 of ($download*) and 1 of ($decode*) and 1 of ($reflect*)
}
