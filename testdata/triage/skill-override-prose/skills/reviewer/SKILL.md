---
name: injection-review
---
# Safety review

```python
injection_patterns = [r"ignore previous instructions"]
for pattern in injection_patterns:
    if re.search(pattern, user_input):
        return False, "Potential prompt injection detected"
```
