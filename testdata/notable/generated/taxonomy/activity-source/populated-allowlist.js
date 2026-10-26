const allowList = ['example.invalid'];
const absent = allowList.indexOf('another.invalid') === -1;
console.log(absent);
