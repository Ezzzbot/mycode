from pymodbus.client import ModbusSerialClient


client = ModbusSerialClient(port='COM1')
print(dir(client))

