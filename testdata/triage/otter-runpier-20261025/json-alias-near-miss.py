def save(value, other):
    import json as codec
    with open("args.json", "w") as stream:
        other.dump(value, stream)
