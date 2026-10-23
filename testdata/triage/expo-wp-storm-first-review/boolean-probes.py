def original(c):
    return f"0) AND ({c})-- -"
def renamed(condition):
    return f"0) AND ({condition})-- -"
def union(rows):
    return f"0) AND 1=0 UNION ALL {rows}"
