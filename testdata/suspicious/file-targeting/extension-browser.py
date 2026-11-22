import os
PATTERNS = ["*.pem", "*.key", "*.sql", "*.conf", "*.db", "*.sqlite"]
def browse(path):
    return os.listdir(path)
