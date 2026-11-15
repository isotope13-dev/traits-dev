import base64


def load_index(index_path):
    with open(index_path, "rt", encoding="utf-8") as index_file:
        encoded_index = index_file.read()
    return base64.b64decode(encoded_index).decode("utf-8")
