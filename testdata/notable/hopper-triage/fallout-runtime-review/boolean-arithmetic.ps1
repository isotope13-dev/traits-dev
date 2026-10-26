$a=3;$b=5;$p=($a -band -bnot $b) -bor (-bnot $a -band $b); Write-Output $p
