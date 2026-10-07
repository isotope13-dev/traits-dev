class Stager:
    def __init__(self, mainMenu):
        self.options = {
            'Listener': {'Description': 'Listener to generate stager for.', 'Value': ''},
            'Obfuscate': {'Description': 'Obfuscate the launcher powershell code.', 'Value': 'False'},
        }

    def generate(self):
        launcher = self.mainMenu.stagergenv2.generate_launcher()
        pkt = self.mainMenu.packets.build_routing_packet(b'stage0')
        return launcher + pkt.hex()
