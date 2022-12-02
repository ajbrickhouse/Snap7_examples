"""
Example ussage of the read_multi_vars function

This was tested against a S7-319 CPU
"""

import ctypes

import snap7
from snap7.common import check_error
from snap7.types import S7DataItem, S7AreaDB, S7WLByte
from snap7.util import *

client = snap7.client.Client()
client.connect('192.168.0.1', 0, 0)

data_items = (S7DataItem * 4)()

data_items[0].Area = ctypes.c_int32(S7AreaDB)
data_items[0].WordLen = ctypes.c_int32(S7WLByte)
data_items[0].Result = ctypes.c_int32(0)
data_items[0].DBNumber = ctypes.c_int32(54) # Datablock #
data_items[0].Start = ctypes.c_int32(16)    # Offset
data_items[0].Amount = ctypes.c_int32(4)  # length of bytes - reading a REAL, 4 bytes

data_items[1].Area = ctypes.c_int32(S7AreaDB)
data_items[1].WordLen = ctypes.c_int32(S7WLByte)
data_items[1].Result = ctypes.c_int32(0)
data_items[1].DBNumber = ctypes.c_int32(54)
data_items[1].Start = ctypes.c_int32(60)
data_items[1].Amount = ctypes.c_int32(6)  # reading a DINT, 6 bytes

data_items[2].Area = ctypes.c_int32(S7AreaDB)
data_items[2].WordLen = ctypes.c_int32(S7WLByte)
data_items[2].Result = ctypes.c_int32(0)
data_items[2].DBNumber = ctypes.c_int32(54)
data_items[2].Start = ctypes.c_int32(12)
data_items[2].Amount = ctypes.c_int32(2)  # reading an INT, 2 bytes

data_items[3].Area = ctypes.c_int32(S7AreaDB)
data_items[3].WordLen = ctypes.c_int32(S7WLByte)
data_items[3].Result = ctypes.c_int32(0)
data_items[3].DBNumber = ctypes.c_int32(54)
data_items[3].Start = ctypes.c_int32(14)
data_items[3].Amount = ctypes.c_int32(2)  # reading an BOOL, 2 bytes

# create buffers to receive the data
# use the Amount attribute on each item to size the buffer
for di in data_items:
    # create the buffer
    buffer = ctypes.create_string_buffer(di.Amount)

    # cast the pointer to the buffer to the required type
    pBuffer = ctypes.cast(ctypes.pointer(buffer),
                          ctypes.POINTER(ctypes.c_uint8))
    di.pData = pBuffer

result, data_items = client.read_multi_vars(data_items)

for di in data_items:
    check_error(di.Result)

result_values = []
# function to cast bytes to match data_types[] above
byte_to_value = [get_real, get_dint, get_int, get_bool]

# unpack and test the result of each read
for i in range(0, len(data_items)):
    btv = byte_to_value[i]
    di = data_items[i]

    if "get_bool" in str(btv):
        value = btv(di.pData, 0, 0)
    else:
        value = btv(di.pData, 0)

    result_values.append(value)

result_values.append(f"CPU State: ({client.get_cpu_state()})")
result_values.append(f"Connected?: ({client.get_connected()})")

print(result_values)

client.disconnect()
client.destroy()