# Interactive history recall example from a PowerShell admin template.
Get-History | Out-GridView -PassThru | Invoke-Expression
