let a = unescape('%u4141%u4141');
let b = a;
for (let i = 0; i < 32; i++) {
 a += b;
 b += a;
 a += b;
 b += a;
}
document.write(a);
