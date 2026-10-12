- id: callback-sample
- language: php
- vulnerable: true
- detector: callback_dispatch

```php
<?php call_user_func($_GET['callback']);
```
