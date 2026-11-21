def atom(value):
    return value

def other(value):
    return value

def tup(*values):
    return values

# Distinct encoders do not establish a matching encoded MFA pair.
mfa = tup(atom(r"erpc"), other(r"execute_call"))
args = [atom(r"os"), other(r"cmd")]
