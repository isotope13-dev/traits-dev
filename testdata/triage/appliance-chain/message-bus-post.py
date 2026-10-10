class Bus:
    def post(self, message):
        print(message)

bus = Bus()
bus.post('event')
