rule Concealed_URL_ClassLoader_Stage
{
    meta:
        description = "Java stage reflectively builds a URL-array class loader and invokes a hex-concealed member"
        scan_context = "file"

    strings:
        $url_array = "[Ljava/net/URL;" ascii
        $forname = "forName" ascii
        $getctor = "getConstructor" ascii
        $newinst = "newInstance" ascii
        $getmethod = "getMethod" ascii
        $invoke = "invoke" ascii
        $hex_member = /_[0-9a-f]{32}/ ascii

    condition:
        $url_array and $forname and $getctor and $newinst and $getmethod and
        $invoke and $hex_member
}
