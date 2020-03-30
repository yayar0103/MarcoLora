# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 18:50:36 2020

@author: yayar
"""
import LoRa

x = LoRa.LoRa(port="COM3")
x.display_info()
x.set_mode("rx")
while True:
    # print(x.read())
    received = x.read()
    if received == None:
        continue
    elif received == "remote quit":
        break
    else:
        print(received)
        print("-------------------")

x.close()
print("End Program")
    
    