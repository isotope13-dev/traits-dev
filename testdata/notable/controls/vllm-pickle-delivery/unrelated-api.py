class Store:
    def send_obj(self, obj, dst):
        self.last = obj
peer = Store()
peer.send_obj(obj={"temperature": 21}, dst=0)
