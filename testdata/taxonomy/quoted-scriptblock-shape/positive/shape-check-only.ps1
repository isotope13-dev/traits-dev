function Test-WrapperShape {
    param($Ast)
    # Defensive allowlist: the constructor below is compared as quoted data
    # to recognize a known wrapper shape. Nothing here executes it.
    $decoders = @($Ast.FindAll({ param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -ceq 'D' }, $false))
    if ($decoders.Count -ne 1 -or ($decoders[0].Extent.Text -replace '\s', '') -cne 'function D([string]$v){[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($v))}') { return $false }
    $sb = @($Ast.FindAll({ param($n) $n -is [Management.Automation.Language.AssignmentStatementAst] }, $false))
    if (($sb[0].Right.Extent.Text -replace '\s', '') -cne '[ScriptBlock]::Create($text)') { return $false }
    return $true
}
