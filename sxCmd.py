# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 21:38:24 2020

@author: Steven
"""


import chipIO
import re

class sxCmd(chipIO.chipIO):
    
    def __init__(self, port, baudrate=115200, freq=91500, power=15, auto_connect=False):
        super().__init__(port, baudrate)
        self.chipVer = None
        self.firmWareVer = None
        self.deviceID = None
        self.mode = None
        self.freq = freq
        self.power = power
        self.prevDataID = bytes([0, 0])
        
        if auto_connect == False:
            self.ping()
            self.reset()
            self.get_status()
        
    def ping(self):
        pingCmd = [0x80, 0x00, 0x00]
        response = super().sendCmd(pingCmd)
        if response == False:
            return False
        if self.check_header("^808006(c1|c2)", response.hex()) == True:
            self.chipVer = response[3]
            self.firmWareVer = response[4]
            self.deviceID = response[5:9].hex()
            return True
        else:
            return False
        
    def reset(self):
        resetCmd = [self.chipVer, 0x01, 0x00]
        response = super().sendCmd(resetCmd)
        if self.check_success(response) == True:
            return self.get_status()
        return False
            
        
    def get_status(self):
        statusCmd = [self.chipVer, 0x02, 0x00]
        response = super().sendCmd(statusCmd)
        if self.check_header("^(c1|c2)8208", response.hex()) == True:
            self.mode = response[3]
            self.freq = int.from_bytes(response[4:7], "big")
            self.power = response[7]
            return True
        else:
            return False
    
    
    def setting(self, mode=None, freq=None, power=None):
        if mode is None:
            mode = self.mode
        if freq is None:
            freq = self.freq
        if power is None:
            power = self.power
            
        tmp_f = freq.to_bytes(3, "big")
        
        settingCmd = [self.chipVer, 0x03, 0x05, mode, tmp_f[0], tmp_f[1], tmp_f[2], power]
        response = super().sendCmd(settingCmd)
        if self.check_success(response) == True:
            if mode == 3:
                self.prevDataID = self.get_readCnt()
            return self.get_status()
        else:
            print("Setting Failed")
            return False
        
    def write(self, data):
        data_len = len(data)
        writeCmd = [self.chipVer, 0x05]
        
        writeCmd.append(data_len)
        for letter in str(data):
            writeCmd.append(ord(letter))
        
        response = super().sendCmd(writeCmd)
        if self.check_success(response) == True:
            return True
        else:
            return False
        
    def read(self):
        readCmd = [self.chipVer, 0x06, 0x00]
        response = super().sendCmd(readCmd)
        if self.check_header("^(c1|c2)86", response.hex()) == True:
            data_len = response[2]
            data = response[3:data_len+1]
            content = str()
            for letter in data:
                content += chr(letter)
            return content
        return False
    
    def get_readCnt(self):
        cntCmd = [self.chipVer, 0x07, 0x00]
        response = super().sendCmd(cntCmd)
        return response[3:5]
    
    def check_header(self, pattern, string):
        if type(re.match(pattern, string)) ==  re.Match:
            return True
        else:
            return False
    
    def check_success(self, data):
        if self.chipVer == 0xc1:
            pattern = "c1aa01553f"
        elif self.chipVer == 0xc2:
            pattern = "c2aa01553c"

        if self.check_header(pattern, data.hex()) == True:
            return True
        else:
            return False
        
    def close(self):
        self.setting(mode=1)
        super().closePort()