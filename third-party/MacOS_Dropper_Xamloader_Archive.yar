rule MacOS_Dropper_Xamloader_Archive
{
    meta:
        description = "Detects the Xamloader ZIP archive layout by central-directory names and embedded analyst note"
        author = "OpenAI Codex"
        date = "2026-03-21"
        family = "Xamloader"
        platform = "macOS"
        category = "dropper"

    strings:
        $dir = "Xamloader/" ascii
        $readme = "Xamloader/readme.txtUT" ascii
        $dmg = "Xamloader/Xamloader.dmgUT" ascii
        $avira = "https://www.avira.com/en/support-threats-summary/tid/29207/threat/ADWARE.OSX.Xamloader.A.1" ascii

    condition:
        filesize > 200KB and filesize < 800KB and all of them
}
