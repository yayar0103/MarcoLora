# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 16:22:37 2020

@author: Steven
"""


import serial
import time

class chipIO:

    def __init__(self, port, baudrate):
        self.__ser = None
        self.portPath = port
        self.__baudrate = baudrate
        self.openPort()
        
    def openPort(self):
        self.__ser = serial.Serial(self.portPath, self.__baudrate, timeout=3, writeTimeout=1)
        
    def closePort(self):
        if __debug__ == True:
            print("Port closed")
        self.__ser.close()
        
    def is_open(self):
        return self.__ser.is_open
    
    def serialWrite(self, inp_data):
        try:
            out_data = self.__appendCRC(inp_data)
            self.__ser.write(serial.to_bytes(out_data))
            return True
        except:
            return False
            
    def serialRead(self):
        bytesToRead = self.__ser.inWaiting()
        readData = self.__ser.read(bytesToRead)
        if self.__checkCRC(readData) == True:
            return readData
        else:
            print("Packet Loss")
            
    def sendCmd(self, inp_data):
        if self.serialWrite(inp_data) == True:
            time.sleep(0.04)
            out_data = self.serialRead()
            return out_data
        else:
            return False
    
    def __calCRC(self, data):
        crc = 0
        for i in data:
            crc = crc^i
        return crc
    
    def __appendCRC(self, data):
        crc = self.__calCRC(data)
        data.append(crc)
        return data
    
    def __checkCRC(self, data):
        crc = self.__calCRC(data[:-1])
        if crc == data[-1]:
            return True
        else:
            return False
    
    def __del__(self):
        self.closePort()
        if __debug__ == True:
            print("Destructor called")