# Different encoder receivers do not establish a matching term pair.
def build(first, second, tup, lst):
    mfa = tup(first.atom("erpc"), second.atom("execute_call"), 4)
    args = lst([first.atom("os"), second.atom("cmd"), "id -u"])
    return mfa, args
