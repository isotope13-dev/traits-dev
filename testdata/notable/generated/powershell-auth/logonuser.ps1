[NativeMethods]::LogonUserW($user, $domain, $password, 2, 0, [ref]$token)
[NativeMethods]::LogonUserExW($user, $domain, $password, 2, 0, [ref]$token)
[NativeMethods]::LogonUserExExW($user, $domain, $password, 2, 0, $groups, [ref]$token)
