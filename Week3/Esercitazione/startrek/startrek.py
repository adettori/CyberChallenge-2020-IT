import pyshark
import matplotlib.pyplot as plt
import numpy as np

cap = pyshark.FileCapture('./decloaked.pcap', display_filter='frame.len == 81', use_json=True, include_raw=True)

list_x = []
list_y = []
list_z = []
list_limit = [23, 31, 57, 71, 85, 99, 117, 131, 145, 153, 169, 183, 211, 221, 243, 255, 269, 279, 295, 315, 335, 353, 369, 397, 423]

temp_x = []
temp_y = []
temp_z = []

for packet in cap:
    modbus = packet["MODBUS"]
    frame_n = int(modbus.request_frame)
    
    for x in list_limit:
        if(frame_n <= x):
            list_z.append(list_limit.index(x))
            temp_z.append(list_limit.index(x))

    reg1 = int(modbus.get_field_value("register_0_(uint16)").regval_uint16)
    reg2 = int(modbus.get_field_value("register_1_(uint16)").regval_uint16)

    temp_x.append(reg1)
    temp_y.append(reg2)
    
    if(frame_n in list_limit):
        print(temp_x)
        print(temp_y)
        plt.plot(temp_x, temp_y)
        plt.show()
        temp_x = []
        temp_y = []
        temp_z = []

    list_x.append(reg1)
    list_y.append(reg2)
