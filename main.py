# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 20:33:27 2020

@author: yayar
"""
from scipy import signal
import numpy as np
import soundfile as sf
from ftplib import FTP
import os
import LoRa
import time
import L76X

def dele_files(path_dele):
    ftp = FTP()
    timeout = 172800
    port = 21
    ftp.connect('169.254.220.87', port, timeout)    # 連線FTP伺服器
    ftp.login('yayar')                              # 登入
    ftp.cwd('/home/icListen/Data')                  # 設定FTP路徑
    files = ftp.nlst()                              # 獲得目錄列表   
    for name in files:
        print(name)                                 # 列印檔名字
        path = path_dele + '/' + name
        f = open(path, 'wb')                    # 開啟要儲存檔案
        filename = 'RETR ' + name                   # 儲存FTP檔案
        ftp.retrbinary(filename, f.write)           # 儲存FTP上的檔案
        ftp.delete(name)
    ftp.quit()                                      # 退出FT    

def get_time():
    x=L76X.L76X()
    x.L76X_Set_Baudrate(115200)
    x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_9600)
    time.sleep(2)
    x.L76X_Send_Command(x.SET_POS_FIX_400MS)
    x.L76X_Send_Command(x.SET_NMEA_OUTPUT)
    x.L76X_Exit_BackupMode()
    print('----------------------------------')
    x.L76X_Gat_GNRMC()
    lora = LoRa.LoRa(port='/dev/ttyACM0')
    lora.set_mode("tx")
    print('[data information]:')
    if(x.Status == 1):
        print('Already positioned')
        T = 'Time= ' + str(x.Time_H) +':'+ str(x.Time_M) +':'+ str(x.Time_S)
        print(T)
        P = 'position= '+ str(x.Lat) + str(x.Lat_area) + ',' +str(x.Lon) + str(x.Lon_area)
        print(P)
        x.L76X_Google_Coordinates(x.Lat, x.Lon)
        GP = 'Google= ' + str(x.Lat_Goodle) +','+ str(x.Lon_Goodle)
        print(GP)
        lora.write(T)
        time.sleep(0.5)
        lora.write(P)
        time.sleep(0.5)
        lora.write(GP)
    else:
        N = 'No positioning'
        print(N)
        lora.write(N)

def ftp_get_files(path_ori):
    ftp = FTP()
    timeout = 172800
    port = 21
    ftp.connect('169.254.220.87', port, timeout) 
    ftp.login('yayar') 
    ftp.cwd('/home/icListen/Data')    
    files = ftp.nlst() 
    while files == None:
        time.sleep(10)
        files = ftp.nlst()
    files_first = files[0]
    folder_name = files_first.split('.')[0]   
    os.mkdir(path_ori + folder_name)   
    for name in files:
        print(name)            
        path = path_ori + folder_name + '/'+ name    
        f = open(path,'wb')        
        filename = 'RETR ' + name  
        ftp.retrbinary(filename, f.write) 
        ftp.delete(name)
    ftp.quit()                  
    return path_ori + folder_name

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

def get_dBdata(file, sesty):
    print('Start to  processing the data!')
    audioInfo = sf.info(file)                 # 讀取音訊資訊
    samplerate = audioInfo.samplerate
    frames = audioInfo.frames
    duration = int(audioInfo.duration)
    
    sen_energy = 10**(sesty/10)               # 轉換敏感度 分貝 -> 能量
    presureStan = 10**(-7)
    
    pysData, pysSr = sf.read(file)            # 讀取音訊檔的音訊資料
    nyquistRate = samplerate/2.0
    centerFeq = np.array([19.95, 25.12, 31.62, 39.81, 50.12, 63.10, 79.43, 100, 125.89, 158.49, 199.53, 251.19, 316.23, 398.11, 501.19, 630.96, 794.33,
                        1000, 1258.93, 1584.89, 1995.26, 2511.89, 3162.28, 3981.07, 5011.87, 6309.57, 7943.28, 10000, 12589.25, 15848.93, 19952.62])
    factor = np.power(2, 1/6)
    lowerFeq=centerFeq/factor
    upperFeq=centerFeq*factor
    
    all_dB = np.zeros((32,duration))          # 建立存放最後資訊空矩陣
    freq_cnt = 0
    for lower, upper in zip(lowerFeq, upperFeq):
        sos = signal.butter(10, Wn=np.array([lower, upper])/nyquistRate, btype='bandpass', analog=False, output='sos') 
        filteredData = signal.sosfilt(sos, pysData)
         
        sec_cnt = 0
        print("The " + str(freq_cnt) + " freqency!")
        for start_frames in range(0, frames, samplerate):
            if (sec_cnt == int(duration)):
                break
            end_frames = start_frames + samplerate  
    
            prs_value = (np.sqrt(np.sum(filteredData[start_frames:end_frames]**2)/samplerate))/presureStan
            prs_value += sen_energy
            dB_value = 20*np.log10(prs_value)
            all_dB[freq_cnt][sec_cnt] = round(dB_value)
            sec_cnt += 1        
        freq_cnt += 1 
    float_dB = all_dB/10                      # 各分頻dB累加
    for i in range(duration):
        all_dB[31][i] = round(10*np.log10(np.sum(np.power(10,float_dB[:,i]))), 1)
    return all_dB[31][:]

def get_output(file, datas):
    name = file.split('.')[0]
    t = name.split('_')[3]
    h = t[0:2]
    m = t[2:4]
    s = t[4:6]
    S = int(s) + 45
    M= int(m) + 56
    H = int(h) + 7
    output = []
    for data in datas:
        if S > 60:
            M += (S//60) 
            S -= 60
        if M > 60:
            H += (M//60)
            M -= 60  
        if H > 24:
            H -= 24
        T = str(H) +':'+ str(M)+':'+ str(S)
        output.append(str(T) + ' - ' + str(data))
        S += 1
    return output

def save_totxt(file, output):
    name = file.split('.')[0]
    save =  name + ".txt"
    with open(save, "a") as s:
        for i in output:
            s.write(str(i) + "\n")
    s.close()
    
def sent_lora_min(output):
    lora = LoRa.LoRa(port='/dev/ttyACM0')
    lora.set_mode("tx")
    for data in output:
        print(data)
        lora.write(data)
        time.sleep(0.5)
    lora.close()
    
if __name__ == "__main__":
    path = '/home/pi/Desktop/thesis/data/'
    dele_path = '/home/pi/Desktop/thesis/data/dele'
    sensity = -112
    dele_files(dele_path)
    print('Wating for data input!')
    time.sleep(20)
    get_time()
    while True:
        datapath = ftp_get_files(path)
        files_datas = files_get_wav(datapath)
        for file in files_datas:
            dBdatas = get_dBdata(file, sensity)
            output = get_output(file, dBdatas)
            save_totxt(file, output)      
            sent_lora_min(output)
    
    
   



