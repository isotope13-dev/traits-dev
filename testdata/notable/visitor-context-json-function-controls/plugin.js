// formula engine compiling user-defined formulas
fetch("/formulas.json").then(function (r) { return r.text(); }).then(function (t) {
  var list = JSON.parse(t);
  for (var i = 0; i < list.length; i++) { var f = new Function(list[i])(); register(f); }
  console.log(document.title);
});
