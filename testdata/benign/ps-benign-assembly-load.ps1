function Import-PluginAssembly
{
    param([String]$Path)
    # Legitimate plugin loader: no Empire wrapper function, no encoded blob.
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    return [System.Reflection.Assembly]::Load($bytes)
}
