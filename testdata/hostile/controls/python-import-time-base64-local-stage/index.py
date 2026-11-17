import base64


class Index:
    def run_index(self, path):
        with open(path, "rt", encoding="utf-8") as stage_file:
            stage = base64.b64decode(stage_file.read()).decode("utf-8")
        exec(stage)
