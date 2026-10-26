import operator

def combine(left, right):
    return (left ^ right) ^ operator.xor(left, right)
