base="/pro" + f"c/{pid}"
maps="/m"+"aps"
mem="/m"+"em"
left.seek(start)
try:
    chunk=right.read(end-start)
except OSError:
    pass
