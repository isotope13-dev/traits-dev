def atom(value):
    return value.encode()
def tup(*values):
    return b"".join(values)
mfa = tup(atom(r"erpc"), atom(u"execute_call"))
args = [atom(r"os"), atom(u"cmd")]
