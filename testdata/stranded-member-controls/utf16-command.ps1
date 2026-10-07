foreach ($char in $command.ToCharArray()) { $SMB_relay_command += "{0:X2}-00-" -f [int][char]$char }
