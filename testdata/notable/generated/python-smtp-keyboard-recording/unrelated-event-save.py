class DocumentEditor:
    def receive(self, event):
        self.save(event.document)
    def save(self, value):
        with open('document.txt', 'w') as output:
            output.write(value)
