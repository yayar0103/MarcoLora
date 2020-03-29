# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 20:33:27 2020

@author: yayar
"""
from scipy import signal
import numpy as np
import soundfile as sf
from ftplib import FTP as ftp
import os
import LoRa
import time

def ftp_get_files(path_ori):
    timeout = 172800
    port = 21
    ftp.connect('169.254.220.87', port, timeout) # 連線FTP伺服器
    ftp.login('yayar') # 登入
    ftp.cwd('/home/icListen/Data')    # 設定FTP路徑
    files = ftp.nlst()       # 獲得目錄列表
    files_first = files[0]
    folder_name = files_first.split('.')[0]
    print(folder_name)    
    os.mkdir(path_ori + folder_name)    #創建儲存資料的資料夾
    for name in files:
        print(name)             # 列印檔名字
        path = path_ori + folder_name + '/'+ name    # 檔案儲存路徑
        f = open(path,'wb')         # 開啟要儲存檔案
        filename = 'RETR ' + name   # 儲存FTP檔案
        ftp.retrbinary(filename, f.write) # 儲存FTP上的檔案
        ftp.delete(name)
    ftp.quit()                  # 退出FT  
    return path

def files_get_wav(path):
    datafiles = []
    data_path = os.path.abspath(path)
    for dirPath, dirNames, fileNames in sorted(os.walk(data_path)):   
        for f in sorted(fileNames):
            inputFile = os.path.join(dirPath, f)
            lastFile = os.path.splitext(f)[-1]
            if lastFile == ".wav": 
                 datafiles.append(inputFile)
    return datafiles

def pysound_input_wav(path, startF, endF):   
    pysData, pysSr = sf.read(path, start = startF, stop = endF, dtype = 'int32')
    pysData = pysData/(2**23 - 1)/256
    return pysData

def octave_filtered(data,samr):
    nyquistRate = samr/2.0
    centerFeq = np.array([16, 20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800,
                        1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000])
    
    factor = np.power(2, 1.0/6.0)
    lowerFeq=centerFeq/factor;
    upperFeq=centerFeq*factor;
    rmsData = []
    presureStan = 10**(-6)
    for lower,upper in zip(lowerFeq, upperFeq):
        sos = signal.butter(1, Wn=np.array([lower, upper])/nyquistRate, btype='band', analog=False, output='sos');
        filteredData = signal.sosfilt(sos, data)
        value = ((np.sum(filteredData**2)/31)**0.5)/presureStan
        rmsData.append(value)
    return rmsData

def db_third_datas(rmsdata, cnt):
    dbData = 20*np.log10(rmsdata)
    return dbData

def db_data(dbdata):
    dbdata_float = dbdata/10
    exp_data = []
    for i in dbdata_float:
        exp_data.append(10**i)
    dB = 10*np.log10(np.sum(exp_data))
    return dB

def get_dBdata(file):    #給一個一分鐘長度的wav檔案，輸出60個dB值
    name = (file.split('.')[0]).split('_')
    file_name = 
    audioInfo = sf.info(file)
    samplerate = audioInfo.samplerate  #64000
    frames = audioInfo.frames          #3776000
    counter = 1
    dB_data = []
    for start_frames in range(1, frames-samplerate+2, samplerate):  #1~3712001, 64000
        end_frames = start_frames + samplerate - 1           #63999
        print("The " + str(counter) + "s data!")
        pysound_data = pysound_input_wav(file, start_frames, end_frames)
        rms_data = octave_filtered(pysound_data , samplerate)
        datas = db_third_datas(rms_data, counter)
        dB_data.append(db_data(datas))
        counter += 1
    return dB_data

def save_totxt(file, data):
    name = file.split('.')[0]
    save =  name + ".txt"
    with open(save, "a") as s:
        for i in data:
            s.write(str(i) + "\n")
    s.close()
    
def sent_lora_min(datas):
    lora = LoRa.LoRa()
    lora.set_mode("tx")
    for data in datas:
        lora.write(data)
    lora.close()
    
if __name__ == "__main__":
    path = '/home/pi/Desktop/lora_gps/data/'
    datapath = ftp_get_files(path)
    files_datas = files_get_wav(datapath)    #從資料夾讀取所有wav檔
    for file in files_datas:                 #一個一個讀取wav檔
        dBdatas = get_dBdata(file)           #得到每個wav輸出60個dB值
        save_totxt(file, dBdatas)      
        sent_lora_min(dBdatas)
            
    
    
   



