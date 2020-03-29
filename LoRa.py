# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 10:06:51 2020

@author: Steven
"""


import sxCmd
import serial.tools.list_ports

class LoRa:
    
    def __init__(self, port=None, baudrate=115200, freq=91500, power=15):
        if port is None:
            all_ports = self.listPorts()
            lora_ports = self.listLoRa(all_ports)
            if not lora_ports is None:
                self.lora = sxCmd.sxCmd(lora_ports[0])
            else:
                raise("Please specify which LoRa port to connect")
        else:
            self.lora = sxCmd.sxCmd(port)
    
    def display_info(self):
        chipDict = {0xc1: "Sx1272", 0xc2: "Sx1276"}
        modeDict = {0x00: "Sleep", 0x01: "Standby", 0x02: "TX", 0x03: "RX"}
        print("Port path:", self.lora.portPath)
        print("Chip Version:", chipDict[self.lora.chipVer])
        print("Firmware Version:", self.lora.firmWareVer)
        print("Device ID:", self.lora.deviceID)
        print("Frequency: {:.2f}MHz".format(self.lora.freq/100))
        print("Power: ", str(self.lora.power+2) + "dBm")
        print("Mode:", modeDict[self.lora.mode])
    
    def set_mode(self, mode):
        modeDict = {'sleep': 0x00, 'standby': 0x01, 'tx': 0x02, 'rx': 0x03}
        return self.lora.setting(mode=modeDict[mode])
    
    def set_freq(self, freq):
        if not (86000 <= freq <= 102000):
            print("Frequency out of range")
            return False
        return self.lora.setting(freq=freq)
        
    def set_power(self, power):
        if not (0 <= power <= 15):
            print("Power out of range")
            return False
        return self.lora.setting(power=power)
    
    def write(self, data):
        return self.lora.write(data)
    
    def read(self):
        if self.lora.prevDataID != self.lora.get_readCnt():
            data = self.lora.read()
            self.lora.prevDataID = self.lora.get_readCnt()
            return data
        
    def listPorts(self):
        ports = serial.tools.list_ports.comports()
        for index, port in enumerate(ports):
            print("  " + str(index+1) + ". " + port.device)
        print(str(len(ports)) + " ports found")
        return ports
    
    def listLoRa(self, ports):
        lora_port = []
        for port in ports:
            tmp_port = sxCmd.sxCmd(port=port.device, auto_connect=True)
            if tmp_port.ping() == True:
                lora_port.append(port.device)
            tmp_port.closePort()
                
        if lora_port != None:
            for index, port in enumerate(lora_port):
                print("  " + str(index+1) + ". " + port)
            print(str(len(lora_port)) + " ports found")
            return lora_port
        else:
            raise OSError('No LoRa device found.')
    
    def close(self):
        self.lora.close()
    
if __name__ == "__main__":
    import time
    x = LoRa()
    x.display_info()
    x.set_mode("tx")
    x.write("Hello World")
    time.sleep(0.01)
    x.set_mode("rx")
    input()
    print(x.read())
    x.close()