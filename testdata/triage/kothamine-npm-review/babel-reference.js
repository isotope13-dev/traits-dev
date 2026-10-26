import * as babel from "@babel/core";
const ast = babel.parse("const n = 1");
babel.traverse(ast, {Identifier(p){p.node.name="n"}});
