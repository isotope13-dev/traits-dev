from pymodbus.client import ModbusTcpClient

def set_register(client):
    client.write_register(10, 25)
