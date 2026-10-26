class Writer:
    def write(self, value):
        self.value = value

writer = Writer()
writer.write('ordinary object state')
