import ast
import operator

OPERATORS = {"+": operator.add, "-": operator.sub}


def calculate(expression):
    node = ast.parse(expression, mode="eval").body
    if not isinstance(node, ast.BinOp) or type(node.op) not in (ast.Add, ast.Sub):
        raise ValueError("unsupported expression")
    return OPERATORS["+" if isinstance(node.op, ast.Add) else "-"](
        node.left.n, node.right.n
    )
