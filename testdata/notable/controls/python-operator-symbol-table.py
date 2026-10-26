# Operator symbol tables enumerate the glyphs as string literals; no
# arithmetic is performed with them here.
op_methods = {
    '__add__': '+',
    '__sub__': '-',
    '__mul__': '*',
    '__truediv__': '/',
}

ops_with_inplace_method = {
    '+', '-', '*', '/', '%', '//', '**', '@', '&', '|', '^', '<<', '>>'}

inplace_operator_methods = {
    '__i' + op_methods[op][2:] for op in ops_with_inplace_method
    if op in op_methods
}
