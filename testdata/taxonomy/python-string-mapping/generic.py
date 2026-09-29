def normalize(subdivision):
    return subdivision.translate(str.maketrans({"-": "_", " ": "_"})).lower()
