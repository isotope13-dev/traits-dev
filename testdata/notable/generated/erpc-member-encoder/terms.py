# Equivalent ETF term construction through an encoder object.
def build(codec, tup, lst):
    mfa = tup(codec.atom(r"erpc"), codec.atom(u"execute_call"), 4)
    args = lst((codec.atom(r"os"), codec.atom(u"cmd"), "id -u"))
    return mfa, args
