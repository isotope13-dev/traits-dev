// Inert codec and table-dispatch test; no host automation.
var shards = [
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
"Ab3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4wAb3Z*7km-19sQp4w",
];
function quote(s) { return s.split("'").join("''"); }
function xor(a,b,i) { a[i] = b[i] ^ 42; }
function dispatch(obj,table) {
obj[table[(0)]]();
obj[table[(1)]]();
obj[table[(2)]]();
obj[table[(3)]]();
obj[table[(4)]]();
obj[table[(5)]]();
obj[table[(6)]]();
obj[table[(7)]]();
obj[table[(8)]]();
}
