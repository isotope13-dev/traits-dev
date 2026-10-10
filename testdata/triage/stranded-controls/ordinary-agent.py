import subprocess
class Agent:
    def __init__(self, staging_key, session):
        self.sessionID=session
        self.tasks={}
    def execute(self, source):
        exec(compile(source, "<string>", "exec"), globals())
        return subprocess.Popen("echo hello",shell=True)
