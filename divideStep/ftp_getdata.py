# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 19:25:28 2020

@author: user
"""

from ftplib import FTP
import os
    
ftp = FTP()
timeout = 30
port = 21
ftp.connect('169.254.220.87',port,timeout) # 連線FTP伺服器
ftp.login('yayar') # 登入
ftp.cwd('/home/icListen/Data')    # 設定FTP路徑
files = ftp.nlst()       # 獲得目錄列表
for name in files:
    print(name)             # 列印檔名字
    times = name.split('_')
    time = times[2]
    print(time)
    path = '/home/pi/Desktop/lora_gps/data'+ time + name    # 檔案儲存路徑
    f = open(path,'wb')         # 開啟要儲存檔案
    filename = 'RETR ' + name   # 儲存FTP檔案
    ftp.retrbinary(filename,f.write) # 儲存FTP上的檔案
    ftp.delete(name)
ftp.quit()                  # 退出FT            

datafiles = []
data_path = os.path.abspath(r"D:\yayar\THESIS\LORA\code\data")
print("現在目錄路徑:" + data_path)

for dirPath, dirNames, fileNames in sorted(os.walk(data_path)): 
    print('dirPath', dirPath)
    print('dirNames', dirNames)
    print('fileNames', fileNames)
    print('---------------')   
    for f in sorted(fileNames):
        inputFile = os.path.join(dirPath, f)
        print("inputFile:" + inputFile)
        lastFile = os.path.splitext(f)[-1]
        print("lastFile" + lastFile)
        print("---------------")
        if lastFile == ".wav": 
            datafiles.append(inputFile)
            
for k in datafiles:
    f = open(k)
    save = (r'D:\yayar\THESIS\LORA\code\puredata\test.txt')
    for data in f.readlines()[30:]:  
        with open(save, "a") as s: 
            s.write(data)
            
    s.close()
    f.close()
    
