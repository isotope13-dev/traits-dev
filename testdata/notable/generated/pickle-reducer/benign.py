import pickle
class Record:
    def __reduce__(self):
        return (str, ("record",))
pickle.dumps(Record())
sock.send_multipart([b"record"])
