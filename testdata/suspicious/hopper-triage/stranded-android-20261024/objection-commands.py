def commands(pattern):
    return ["android root disable", "android sslpinning disable",
            "android keystore list", f'memory search "{pattern}" --string']
