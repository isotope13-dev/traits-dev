import ast
tree = ast.parse(source)
nodes = list(ast.walk(tree))
