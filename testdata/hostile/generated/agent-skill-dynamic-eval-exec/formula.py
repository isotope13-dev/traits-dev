def calculate(expression):
    return eval(expression)


def assign(formula, value):
    exec(f"{formula} = {value}")
