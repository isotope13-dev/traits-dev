import umodbus

def set_registers(instrument):
    instrument.write_registers(10, [25, 26])
