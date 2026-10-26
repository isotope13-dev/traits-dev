foreach ($char in $command.ToCharArray()) { $commandBytes += "{0:X2}-" -f [int][char]$char }
