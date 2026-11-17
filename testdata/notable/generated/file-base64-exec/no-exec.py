import base64


def run_index(index_path):
    with open(index_path, "rt", encoding="utf-8") as index_file:
        encoded_index = index_file.read()
    decoded_index = base64.b64decode(encoded_index).decode("utf-8")
    return decoded_index
