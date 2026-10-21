const snippets = ["return 1", "return 2"];
new Function(snippets[0x0]);
new Function(snippets[0x1]);
new Function(decodeSource());
const guard = new RegExp("(((.+)+)+)+$");
const ctor = target['constructo'+'r'];
