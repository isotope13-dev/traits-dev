import base64

def reload_script(source):
    encoded=base64.b64encode(source).decode('ascii')
    return "import base64\nexec(base64.b64decode('%s'))" % encoded
