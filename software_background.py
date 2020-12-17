# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 16:11:53 2020

@author: yayar
"""

import tkinter as tk
from scipy import signal
import numpy as np
import soundfile as sf
from tkinter import filedialog
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import pandas as pd

window = tk.Tk()
window.title('Acoustic Software')
window.geometry('1000x950')

image = None
im = None
all_db = []
all_energy = []
centerFeq_len = 0
db5s = []
time_str = []

def select_file01():
    file_path = filedialog.askopenfilename()
    var01.set(file_path)

def calculate():
    global result
    global result_energy
    global all_db
    global all_energy
    global centerFeq_len
    global time_str
    global sen_energy
    datapath = str(path_entry.get())
    sensity = float(sencity_entry.get())
    
    name = datapath.split('.')[0]
    t = name.split('_')[-1]
    h = t[0:2]
    m = t[2:4]
    s = t[4:6]
    S = int(s) + 45
    M = int(m) + 56
    H = int(h) + 7
    
    sen_energy = 1/(10**(sensity/20))
    audioInfo = sf.info(datapath)
    samplerate = audioInfo.samplerate  
    frames = audioInfo.frames         
    duration = int(audioInfo.duration)
    
    pysData, pysSr = sf.read(datapath)
    pysData = pysData * 3
    nyquistRate = samplerate/2.56
    centerFeq = np.array([16, 20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800,
                            1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000])
    centerFeq_len = len(centerFeq)
    factor = np.power(2, 1/6)
    lowerFeq=centerFeq/factor
    upperFeq=centerFeq*factor
    
    all_energy = np.zeros((centerFeq_len + 1, duration))
    freq_cnt = 0
    for lower, upper in zip(lowerFeq, upperFeq):
        sos = signal.butter(10, Wn=np.array([lower, upper])/nyquistRate, btype='bandpass', analog=False, output='sos') 
        filteredData = signal.sosfilt(sos, pysData)
         
        print('The ' + str(freq_cnt) + ' frequency!')
        sec_cnt = 0
        for start_frames in range(0, frames, samplerate):  
            if (sec_cnt == duration):
                break
            if freq_cnt == 0:
                if sec_cnt == 0:
                    S += 0
                else:
                    S += 1
                if S > 60:
                    M += (S//60) 
                    S -= 60
                if M > 60:
                    H += (M//60)
                    M -= 60  
                if H > 24:
                    H -= 24
                T = str(H) +':'+ str(M)+':'+ str(S)
                time_str.append(T)
            
            end_frames = start_frames + samplerate        
            prs_value = (np.sqrt(np.sum(filteredData[start_frames:end_frames]**2)/samplerate))
            all_energy[freq_cnt][sec_cnt] = prs_value*sen_energy
            
            sec_cnt += 1        
        freq_cnt += 1 
        
    for i in range(duration):
        senn = np.sum(all_energy[:,i])
        all_energy[centerFeq_len][i] = senn
        all_db.append(round(20*np.log10(senn), 1))
        
    result_energy = np.sum(all_energy[centerFeq_len, :])/duration
    result_dB = round(20*np.log10(result_energy), 1)
    result_label.configure(text=result_dB)
    
def reset_sensity():
    global result_energy
    global sen_energy
    input_dB = float(cal_entry.get())
    inputdB_enrgy = 10**(input_dB/20)
    energy = result_energy/sen_energy
    newsen_energy = energy/inputdB_enrgy
    new_sen = round(20*np.log10(newsen_energy), 1)
    newsen_label.configure(text=new_sen)
        
        
def leq():
    global all_energy
    global centerFeq_len
    global db5s
    
    for i in range(0, len(all_energy[centerFeq_len][:]), 5):
        j = i + 5
        sum5s = np.sum(all_energy[centerFeq_len, i:j])/5
        db = round(20*np.log10(sum5s), 1)
        db5s.append(db)
    
    db5s = np.array(db5s)
    sort = sorted(db5s)    
    print(sort)
    duration = len(db5s)
    
    L90_dB = str(sort[int(duration * 0.05)])
    L50_dB = str(sort[int(duration * 0.5)])
    L5_dB = str(sort[int(duration * 0.9)])
    
    L90.configure(text=L90_dB)
    L50.configure(text=L50_dB)
    L5.configure(text=L5_dB)
    
def select_file02():
    file_path = filedialog.askdirectory()
    var02.set(file_path)
    
def init(path, num):
    data, fs = sf.read(path)
    second = len(data)/fs
    t = np.linspace(0, second, len(data))
    plt.plot(t, data)
    plt.title('Time domain of the siganl')
    plt.xlabel('Time (s)')
    plt.ylabel('Magntitude')
    plt.grid()
    plt.savefig(str(num) + ".jpg")
    return fs, data   
 
# 使用內建的function將聲音轉成頻域
def spectrogram_(data, fs, sensity, num):
    sen_energy = 10**(sensity/10)
    f, t, Sxx = signal.spectrogram(data, fs, mode='magnitude')    
    for i in range(0, len(Sxx[:,1])):
        for j in range(0, len(Sxx[1,:])):
            Sxx[i,j] += sen_energy
            Sxx[i,j] = 20*np.log10(abs(Sxx[i,j])/10**(-6))
    plt.pcolormesh(t, f, Sxx) 
    plt.title('Spectrogram of the signal')           
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    # plt.clim(0, 50)
    cb = plt.colorbar()
    cb.set_label('Magnitude (dB)')
    plt.savefig(str(num) + "-1.jpg")
    return Sxx

def sepctrum(data, fs, num):  
    # Pxx = plt.psd(data, fs)
    f, Pxx = signal.periodogram(data, fs, 'flattop')
    # Pxx = 20*np.log10(Pxx/10**(-6))
    plt.semilogy(f, Pxx)
    plt.title('Amplitude spectrum of the signal')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('PSD')
    plt.grid()
    plt.savefig(str(num) + "-2.jpg")
    return Pxx

def octave(data, fs, sensity, num):
    nyquistRate = fs/2.56
    centerFeq = np.array([20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800,
                            1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000])
    centerFeq_len = len(centerFeq)
    factor = np.power(2, 1/6)
    lowerFeq=centerFeq/factor
    upperFeq=centerFeq*factor
    sen_energy = 10**(sensity/10)
    presureStan = 10**(-7)  
    
    all_dB = np.zeros(centerFeq_len)
    freq_cnt = 0
    for lower, upper in zip(lowerFeq, upperFeq):
        sos = signal.butter(10, Wn=np.array([lower, upper])/nyquistRate, btype='bandpass', analog=False, output='sos') 
        filteredData = signal.sosfilt(sos, data)
        
        prs_value = (np.sqrt(np.sum(filteredData**2)/fs))/presureStan
        prs_value += sen_energy
        dB_value = 20*np.log10(prs_value)
        all_dB[freq_cnt] = dB_value
        freq_cnt += 1
        
    cF = ['20', '25', '31.5', '40', '50', '63', '80', '100', '125', '160', '200', '250', '315', '400', '500', '630', '800', '1k',
                              '1.25k', '1.6k', '2k', '2.5k', '3.15k', '4k', '5k', '6.3k', '8k', '10k', '12.5k', '16k', '20k']    
    plt.figure()
    plt.plot(cF, all_dB, '--o')
    plt.title("1/3 Octave band presure level")
    plt.xlabel('1/3 Octave band (Hz)')
    plt.ylabel('1/3 Octave band Level (dB re 1e-6Pa)')
    plt.xticks(rotation='vertical')
    plt.grid()
    plt.savefig(str(num) + "-3.jpg")

def wavplot():
    path = str(path_entry.get())
    sensity = float(sencity_entry.get())
    a = path.split('/')[-1]
    b = a.split('.')[0]
    num = str(plotpath_entry.get()) + '/' + str(b)
    fs, b = init(path, num) 
    Sxx = spectrogram_(b, fs, sensity, num) 
    Pxx = sepctrum(b, fs, num)
    octave(b, fs, sensity, num) 
    var02_run.set("完成100%")

def init_show():
    global img
    path = str(path_entry.get())
    a = path.split('/')[-1]
    b = a.split('.')[0]
    num = str(plotpath_entry.get()) + '/' + str(b)
    file = num + '.jpg'
    img = Image.open(file)
    img = ImageTk.PhotoImage(img)   
    canvas.create_image(320,180, anchor='center',image=img)   
    
def spectrogram_show():
    global img
    path = str(path_entry.get())
    a = path.split('/')[-1]
    b = a.split('.')[0]
    num = str(plotpath_entry.get()) + '/' + str(b)
    file = num + '-1.jpg'
    img = Image.open(file)
    img = ImageTk.PhotoImage(img)
    canvas.create_image(320,180, anchor='center',image=img)   
    
def spectrum_show():
    global img
    path = str(path_entry.get())
    a = path.split('/')[-1]
    b = a.split('.')[0]
    num = str(plotpath_entry.get()) + '/' + str(b)
    file = num + '-2.jpg'
    img = Image.open(file)
    img = ImageTk.PhotoImage(img)
    canvas.create_image(320,180, anchor='center',image=img)   
    
def octave_show():
    global img
    path = str(path_entry.get())
    a = path.split('/')[-1]
    b = a.split('.')[0]
    num = str(plotpath_entry.get()) + '/' + str(b)
    file = num + '-3.jpg'
    img = Image.open(file)
    img = ImageTk.PhotoImage(img)
    canvas.create_image(320,180, anchor='center',image=img)  

def save_csv():
    global all_energy
    global time_str
    file_save = filedialog.asksaveasfilename()
    writer = pd.ExcelWriter(file_save)
    db_val = np.around(20*np.log10(all_energy), decimals=1)
    data = {"TIME - 1/3 Octave": time_str[:],
            "20 Hz": db_val[0][:], "25 Hz": db_val[1][:], "31.5 Hz": db_val[2][:],
            "40 Hz": db_val[3][:], "50 Hz": db_val[4][:], "63 Hz": db_val[5][:],
            "80 Hz": db_val[6][:], "100 Hz": db_val[7][:], "125 Hz": db_val[8][:],
            "160 Hz": db_val[9][:], "200 Hz": db_val[10][:], "250 Hz": db_val[11][:],
            "315 Hz": db_val[12][:], "400 Hz": db_val[13][:], "500 Hz": db_val[14][:],
            "630 Hz": db_val[15][:], "800 Hz": db_val[16][:], "1k Hz": db_val[17][:],
            "1.25k Hz": db_val[18][:], "1.6k Hz": db_val[19][:], "2k Hz": db_val[20][:],
            "2.5k Hz": db_val[21][:], "3.15k Hz": db_val[22][:], "4k Hz": db_val[23][:],
            "5k Hz": db_val[24][:], "6.3k Hz": db_val[25][:], "8k Hz": db_val[26][:],
            "10k Hz": db_val[27][:], "12.5k Hz": db_val[28][:], "16k Hz": db_val[29][:],
            "20k Hz": db_val[30][:], "sql 1/3 Octave": db_val[31][:]} 
    table = pd.DataFrame(data)
    table.to_excel(writer, encoding = 'utf-8', sheet_name='Sheet1', index=False)
    writer.save()
    writer.close()
        
              
header_label = tk.Label(window, text='水下聲學背景噪音分析系統', font=('標楷體', 40, 'bold'))
header_label.pack(padx=5, pady=30)

menu = tk.Menu(window)
file_meu = tk.Menu(menu)
menu.add_cascade(label='File', menu=file_meu)
file_meu.add_command(label='SaveAsCsv', command=save_csv)
help_meu = tk.Menu((menu))
menu.add_cascade(label='Help', menu=help_meu)
help_meu.add_command(label='Manual')
window.config(menu=menu)

# 檔案資訊
path_frame = tk.LabelFrame(window, text='檔案資料', font=('標楷體', 10), labelanchor='n')
path_frame.pack()
var01 = tk.StringVar()
path_label = tk.Label(path_frame, text='檔案路徑', font=('標楷體', 12, 'bold'))
path_label.pack(side=tk.LEFT, padx=5, pady=10)
path_entry = tk.Entry(path_frame, textvariable=var01, bd = 5, font=('標楷體', 8), width=50)
path_entry.pack(side=tk.LEFT, padx=5, pady=10)
path_btn = tk.Button(path_frame, text='選取檔案', font=('標楷體', 12, 'bold'), command = select_file01)
path_btn.pack(side=tk.LEFT, padx=5, pady=10)
sencity_label = tk.Label(path_frame, text='敏感度(dB/MPa)', font=('標楷體', 12, 'bold'))
sencity_label.pack(side=tk.LEFT, padx=5, pady=5)
sencity_entry = tk.Entry(path_frame, bd = 5, font=('標楷體', 8), width=15)
sencity_entry.pack(side=tk.LEFT, padx=10, pady=5)
frame = tk.Frame(window)
frame.pack()

# 計算每一次dB值
db_frame = tk.LabelFrame(frame, text='計算最後一秒dB值', font=('標楷體', 10), labelanchor='n')
db_frame.pack(side=tk.LEFT, padx=40)
calculate_btn = tk.Button(db_frame, text='計算每秒dB值', font=('標楷體', 12, 'bold'), command = calculate)
calculate_btn.pack(pady=10)
result_frame = tk.Frame(db_frame)
result_frame.pack()
alldB_label = tk.Label(result_frame, text='最後一秒dB值', font=('標楷體', 12, 'bold'))
alldB_label.pack(side=tk.LEFT, padx=5, pady=10)
result_label = tk.Label(result_frame, bg='Khaki', font=('標楷體', 12), width=10, height=2)
result_label.pack(side=tk.LEFT, padx=10, pady=10)

# 重新設定敏感度
sen_frame = tk.LabelFrame(frame, text='計算每秒dB值', font=('標楷體', 10), labelanchor='n')
sen_frame.pack(side=tk.LEFT, pady=30)
rset_frame = tk.Frame(sen_frame)
rset_frame.pack(side=tk.TOP)
cal_label = tk.Label(rset_frame, text='校正器dB值', font=('標楷體', 12, 'bold'))
cal_label.pack(side=tk.LEFT, padx=5, pady=10)
cal_entry = tk.Entry(rset_frame, bd = 5, font=('標楷體', 8), width=15)
cal_entry.pack(side=tk.LEFT, padx=10, pady=5)
reset_btn = tk.Button(sen_frame, text='重新設定敏感度', font=('標楷體', 12, 'bold'), command = reset_sensity)
reset_btn.pack(padx=5, pady=5)
new_frame = tk.Frame(sen_frame)
new_frame.pack(side=tk.TOP)
newtex_label = tk.Label(new_frame, text='最後輸出敏感度', font=('標楷體', 12, 'bold'))
newtex_label.pack(side=tk.LEFT, padx=5, pady=10)
newsen_label = tk.Label(new_frame, bg='Khaki', font=('標楷體', 12), width=10, height=2)
newsen_label.pack(side=tk.LEFT, padx=10, pady=10)

# 背景Leq
leq_frame = tk.LabelFrame(frame, text='百分率音壓位準（Percentile level）', font=('標楷體', 10), labelanchor='n')
leq_frame.pack(side=tk.LEFT, padx=40)
leq_btn = tk.Button(leq_frame, text='計算背景Leq-5s', font=('標楷體', 12, 'bold'), command = leq)
leq_btn.pack(padx=10, pady=5)
var_run = tk.StringVar()
leq_runtime = tk.Label(leq_frame, textvariable=var_run, font=('標楷體', 12, 'bold'), fg='Red')
leq_runtime.pack()

L90_frame = tk.Frame(leq_frame)
L90_frame.pack(side=tk.LEFT)
L90_text = tk.Label(L90_frame, text='L90', font=('標楷體', 12, 'bold'))
L90_text.pack()
L90 = tk.Label(L90_frame, bg='LightSalmon', font=('標楷體', 12), width=8, height=2)
L90.pack(side=tk.LEFT, padx=10, pady=5)

L50_frame = tk.Frame(leq_frame)
L50_frame.pack(side=tk.LEFT)
L50_text = tk.Label(L50_frame, text='L50', font=('標楷體', 12, 'bold'))
L50_text.pack()
L50 = tk.Label(L50_frame, bg='LightSalmon', font=('標楷體', 12), width=8, height=2)
L50.pack(side=tk.LEFT, padx=10, pady=5)

L5_frame = tk.Frame(leq_frame)
L5_frame.pack(side=tk.LEFT)
L5_text = tk.Label(L5_frame, text='L5', font=('標楷體', 12, 'bold'))
L5_text.pack()
L5 = tk.Label(L5_frame, bg='LightSalmon', font=('標楷體', 12), width=8, height=2)
L5.pack(side=tk.LEFT, padx=10, pady=5)

# 資料視覺化
plot_frame = tk.LabelFrame(window, text='檔案資料視覺化', font=('標楷體', 10), labelanchor='n')
plot_frame.pack(side=tk.TOP, padx=30, pady=5)
plotpath_frame = tk.Frame(plot_frame)
plotpath_frame.pack()
plotpath_label = tk.Label(plotpath_frame, text='選取圖片儲存位置', font=('標楷體', 12, 'bold'))
plotpath_label.pack(side=tk.LEFT, padx=10, pady=10)
var02 = tk.StringVar()
plotpath_entry = tk.Entry(plotpath_frame, textvariable=var02, bd = 5, font=('標楷體', 8), width=50)
plotpath_entry.pack(side=tk.LEFT, padx=5, pady=10)
plotpath_btn = tk.Button(plotpath_frame, text='選取位置', font=('標楷體', 12, 'bold'), command = select_file02)
plotpath_btn.pack(side=tk.LEFT, padx=10, pady=10)
plot_btn = tk.Button(plot_frame, text='資料視覺化', font=('標楷體', 12, 'bold'), command = wavplot)
plot_btn.pack(padx=10, pady=10)
var02_run = tk.StringVar()
plot_runtime = tk.Label(plot_frame, textvariable=var02_run, font=('標楷體', 12, 'bold'), fg='Red')
plot_runtime.pack()

figure_frame = tk.Frame(plot_frame)
figure_frame.pack()
init_btn = tk.Button(figure_frame, text='音訊時域圖', font=('標楷體', 12, 'bold'), command=init_show)
init_btn.pack(side=tk.LEFT)
spectrogram_btn = tk.Button(figure_frame, text='音訊時頻圖', font=('標楷體', 12, 'bold'), command=spectrogram_show)
spectrogram_btn.pack(side=tk.LEFT)
sepctrum_btn = tk.Button(figure_frame, text='音訊頻譜圖', font=('標楷體', 12, 'bold'), command=spectrum_show)
sepctrum_btn.pack(side=tk.LEFT)
octave_btn = tk.Button(figure_frame, text='音訊三分之一倍頻圖', font=('標楷體', 12, 'bold'), command=octave_show)
octave_btn.pack(side=tk.LEFT)

canvas=tk.Canvas(plot_frame, height=550, width=800)
canvas.create_image(300,200, anchor='center')
canvas.pack(pady=20)

window.mainloop()













