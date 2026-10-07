import os
import pickle
class Record:
    def __reduce__(self):
        return (str, ("record",))
    def execute(self):
        return (os.system, ("id",))
pickle.dumps(Record())
