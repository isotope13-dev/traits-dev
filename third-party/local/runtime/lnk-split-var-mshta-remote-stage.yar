rule LNK_SplitVar_Mshta_RemoteStage
{
    meta:
        description = "LNK rebuilds mshta from split environment variables and launches a remote HTA over HTTPS"
        scan_context = "file"

    strings:
        $example = /start "" ![A-Za-z_][A-Za-z0-9_]{0,31}!![A-Za-z_][A-Za-z0-9_]{0,31}! https:\/\/example\.(org|com|net)(:[0-9]+)?[\/" ]/ wide nocase
        $lnk_magic = { 4C 00 00 00 01 14 02 00 }
        $msh = /set [A-Za-z_][A-Za-z0-9_]{0,31}=msh/ wide nocase
        $ta = /set [A-Za-z_][A-Za-z0-9_]{0,31}=ta/ wide nocase
        $start = /start "" ![A-Za-z_][A-Za-z0-9_]{0,31}!![A-Za-z_][A-Za-z0-9_]{0,31}! https:\/\// wide nocase

    condition:
        // Contiguous `set V1=msh&&set V2=ta&&start "" !V1!!V2! https://`
        // with both delayed-expansion names bound to their assignments.
        // Unrelated SETs or undefined variables cannot establish remote
        // MSHTA activation.
        $lnk_magic at 0 and
        for any m in (1..#msh) : (
            for any t in (1..#ta) : (
                @ta[t] == @msh[m] + !msh[m] + 4 and
                uint16(@ta[t] - 4) == 0x26 and
                uint16(@ta[t] - 2) == 0x26 and
                for any s in (1..#start) : (
                    @start[s] == @ta[t] + !ta[t] + 4 and
                    (not $example or for all d in (1..#example) : (
                        @example[d] != @start[s]
                    )) and
                    uint16(@start[s] - 4) == 0x26 and
                    uint16(@start[s] - 2) == 0x26 and
                    !start[s] == 44 + (!msh[m] - 16) + (!ta[t] - 14) and
                    for all i in (0..(((!msh[m] - 16) >> 1) - 1)) : (
                        (uint16(@msh[m] + 8 + i * 2) | 0x20) ==
                        (uint16(@start[s] + 20 + i * 2) | 0x20)
                    ) and
                    for all i in (0..(((!ta[t] - 14) >> 1) - 1)) : (
                        (uint16(@ta[t] + 8 + i * 2) | 0x20) ==
                        (uint16(@start[s] + 24 + !msh[m] - 16 + i * 2) | 0x20)
                    )
                )
            )
        )
}
