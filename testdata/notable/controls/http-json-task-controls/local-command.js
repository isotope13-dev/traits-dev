var cp = require('child_process');
function run(input) {
  var c = JSON.parse(input);
  cp.exec(c.c, function (e, so, se) { console.log({out: so + se}); });
}
run(process.argv[2]);
