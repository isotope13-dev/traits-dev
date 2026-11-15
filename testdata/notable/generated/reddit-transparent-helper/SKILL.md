---
name: reddit-comment-helper
description: A transparent, user-confirmed Reddit comment helper.
---

# Reddit comment helper

The user reviews and confirms every comment before it is submitted. For an
explicitly requested post, this example sends the comment through Reddit's
comment API:

```javascript
let result = await fetch('/api/comment', {
  method: 'POST',
  credentials: 'include',
  body: form.toString()
});
```

The tool does not claim to hide automation.
