# Arithmetic is a capability, including when a token table is also present.
operators = "* / // % & | ^ ~ << >>"
value, scale, width, flags, left, right = 11, 3, 2, 7, 2, 1
result = value * scale // width | flags << left >> right
grouped = ((value * scale) // width | ((flags << left) >> right))
