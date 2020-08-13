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


window = tk.Tk()
window.title('Acoustic Software')
window.geometry('900x900')

result = ''
result_energy = 0

def select_file01():
    file_path = filedialog.askopenfilename()
    var01.set(file_path)

def calculate():
    global result
    global result_energy
    datapath = str(path_entry.get())
    sensity = float(sencity_entry.get())
    
    sen_energy = 1/(10**(sensity/20))
    audioInfo = sf.info(datapath)
    
    samplerate = audioInfo.samplerate  
    frames = audioInfo.frames         
    duration = int(audioInfo.duration)
    
    pysData, pysSr = sf.read(datapath)
    pysData = pysData * 3
    nyquistRate = samplerate/2.56
    centerFeq = np.array([20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800,
                            1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000])
    centerFeq_len = len(centerFeq)
    factor = np.power(2, 1/6)
    lowerFeq=centerFeq/factor
    upperFeq=centerFeq*factor
    
    all_energy = np.zeros((centerFeq_len + 1, duration))
    all_dB = np.zeros((centerFeq_len + 1, duration))
    freq_cnt = 0
    for lower, upper in zip(lowerFeq, upperFeq):
        sos = signal.butter(10, Wn=np.array([lower, upper])/nyquistRate, btype='bandpass', analog=False, output='sos') 
        filteredData = signal.sosfilt(sos, pysData)
         
        print('The ' + str(freq_cnt) + ' frequency!')
        sec_cnt = 0
        for start_frames in range(0, frames, samplerate):  
            if (sec_cnt == duration):
                break
            end_frames = start_frames + samplerate        
            
            prs_value = (np.sqrt(np.sum(filteredData[start_frames:end_frames]**2)/samplerate))
            all_energy[freq_cnt][sec_cnt] = prs_value
            
            prs_value *= sen_energy
            dB_value = 20*np.log10(prs_value)
            
            all_dB[freq_cnt][sec_cnt] = round(dB_value, 4)
            sec_cnt += 1        
        freq_cnt += 1 
        
    float_dB = all_dB/10
    for i in range(duration):
        summ = (np.sum(np.power(10, float_dB[:,i])))
        all_dB[centerFeq_len][i] = round(10*np.log10(summ), 1)
        
    print(all_dB[centerFeq_len][:])
    
    result_energy = np.sum(all_energy[:, duration-1])
    result = str(all_dB[centerFeq_len][duration-1])
    result_label.configure(text=result)
    
def reset_sensity():
    global result
    global result_energy
    cal_sen = float(cal_entry.get())
    cal_sen_enrgy = 10**(cal_sen/20)
    if result != cal_sen:
        new_sen_powr = result_energy/cal_sen_enrgy
    
    new_sen = round(20*np.log10(new_sen_powr), 1)
    newsen_label.configure(text=new_sen)
        
        
def leq():
    datapath = str(path_entry.get())
    sensity = float(sencity_entry.get())
    
    sen_energy = 1/(10**(sensity/20))
    audioInfo = sf.info(datapath)
    
    samplerate = audioInfo.samplerate  
    frames = audioInfo.frames         
    duration = int(audioInfo.duration/5)
    
    pysData, pysSr = sf.read(datapath)
    pysData = pysData * 3
    nyquistRate = samplerate/2.56
    centerFeq = np.array([20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800,
                            1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000])
    centerFeq_len = len(centerFeq)
    factor = np.power(2, 1/6)
    lowerFeq=centerFeq/factor
    upperFeq=centerFeq*factor
    
    all_dB = np.zeros((centerFeq_len + 1, duration))
    freq_cnt = 0
    for lower, upper in zip(lowerFeq, upperFeq):
        sos = signal.butter(10, Wn=np.array([lower, upper])/nyquistRate, btype='bandpass', analog=False, output='sos') 
        filteredData = signal.sosfilt(sos, pysData)
         
        # print('The ' + str(freq_cnt) + ' frequency!')
        run = int(((freq_cnt + 1)/31)*100)
        runtime = '完成度 ' + str(run) + '%'
        print(runtime)
        var_run.set(runtime)
        sec_cnt = 0
        for start_frames in range(0, frames, samplerate*5):  
            if (sec_cnt == duration):
                break
            end_frames = start_frames + samplerate*5        
            
            prs_value = (np.sqrt(np.sum(filteredData[start_frames:end_frames]**2)/samplerate))
            prs_value *= sen_energy
            dB_value = 20*np.log10(prs_value)
            
            all_dB[freq_cnt][sec_cnt] = round(dB_value, 4)
            sec_cnt += 1        
        freq_cnt += 1 
        
    float_dB = all_dB/10
    for i in range(duration):
        summ = (np.sum(np.power(10, float_dB[:,i])))
        all_dB[centerFeq_len][i] = round(10*np.log10(summ), 1)
        
    sort = sorted(all_dB[centerFeq_len][:])    
    print(sort)
    
    L90_pst = int(duration * 0.9)
    L50_pst = int(duration * 0.5)
    L5_pst = int(duration * 0.05)
    
    L90_dB = str(sort[L90_pst])
    L50_dB = str(sort[L50_pst])
    L5_dB = str(sort[L5_pst])
    
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
    plt.show()
    
    return fs, data   
 
# 使用內建的function將聲音轉成頻域
def spectrogram_(data, fs, sensity, num):
    sen_energy = 10**(sensity/10)
    f, t, Sxx = signal.spectrogram(data, fs, mode='magnitude')    #output 時頻譜, scaling='spectrum'
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
    plt.show()
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
    plt.show()
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
        
    cF = ['16', '20', '25', '31.5', '40', '50', '63', '80', '100', '125', '160', '200', '250', '315', '400', '500', '630', '800',
                              '1k', '1.25k', '1.6k', '2k', '2.5k', '3.15k', '4k', '5k', '6.3k', '8k', '10k', '12.5k', '16k']    
    plt.figure()
    plt.plot(cF, all_dB, '--o')
    plt.title("1/3 Octave band presure level")
    plt.xlabel('1/3 Octave band (Hz)')
    plt.ylabel('1/3 Octave band Level (dB re 1e-6Pa)')
    plt.xticks(rotation='vertical')
    plt.grid()
    plt.savefig(str(num) + "-3.jpg")
    plt.show()

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

def init_show():
    global img
    path = str(path_entry.get())
    a = path.split('/')[-1]
    b = a.split('.')[0]
    num = str(plotpath_entry.get()) + '/' + str(b)
    file = num + '.jpg'
    img = Image.open(file)
    img = ImageTk.PhotoImage(img)
    showing = tk.Label(image_frame, image=img).pack(padx=30, pady=10)
    
def spectrogram_show():
    global img
    path = str(path_entry.get())
    a = path.split('/')[-1]
    b = a.split('.')[0]
    num = str(plotpath_entry.get()) + '/' + str(b)
    file = num + '-1.jpg'
    img = Image.open(file)
    img = ImageTk.PhotoImage(img)
    showing = tk.Label(image_frame, image=img).pack(padx=30, pady=10)
    
def spectrum_show():
    global img
    path = str(path_entry.get())
    a = path.split('/')[-1]
    b = a.split('.')[0]
    num = str(plotpath_entry.get()) + '/' + str(b)
    file = num + '-2.jpg'
    img = Image.open(file)
    img = ImageTk.PhotoImage(img)
    showing = tk.Label(image_frame, image=img).pack(padx=30, pady=10)
    
def octave_show():
    global img
    path = str(path_entry.get())
    a = path.split('/')[-1]
    b = a.split('.')[0]
    num = str(plotpath_entry.get()) + '/' + str(b)
    file = num + '-3.jpg'
    img = Image.open(file)
    img = ImageTk.PhotoImage(img)
    showing = tk.Label(image_frame, image=img).pack(padx=30, pady=10)
        
        
        
header_label = tk.Label(window, text='水下背景聲學測量', font=('標楷體', 40, 'bold'))
header_label.pack(padx=5, pady=30)


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
leq_frame = tk.LabelFrame(window, text='計算背景Leq(5s)', font=('標楷體', 10), labelanchor='n')
leq_frame.pack(side=tk.LEFT, padx=40)
leq_btn = tk.Button(leq_frame, text='計算背景Leq-5s', font=('標楷體', 12, 'bold'), command = leq)
leq_btn.pack(padx=10, pady=10)
var_run = tk.StringVar()
leq_runtime = tk.Label(leq_frame, textvariable=var_run, font=('標楷體', 12, 'bold'), fg='Red')
leq_runtime.pack()

L90_frame = tk.Frame(leq_frame)
L90_frame.pack(side=tk.TOP)
L90_text = tk.Label(L90_frame, text='L90', font=('標楷體', 12, 'bold'))
L90_text.pack(padx=10, pady=5)
L90 = tk.Label(L90_frame, bg='LightSalmon', font=('標楷體', 12), width=8, height=2)
L90.pack(side=tk.LEFT, padx=10)
L50_frame = tk.Frame(leq_frame)
L50_frame.pack(side=tk.TOP)
L50_text = tk.Label(L50_frame, text='L50', font=('標楷體', 12, 'bold'))
L50_text.pack()
L50 = tk.Label(L50_frame, bg='LightSalmon', font=('標楷體', 12), width=8, height=2)
L50.pack(side=tk.LEFT, padx=10)
L5_frame = tk.Frame(leq_frame)
L5_frame.pack(side=tk.TOP)
L5_text = tk.Label(L5_frame, text='L5', font=('標楷體', 12, 'bold'))
L5_text.pack()
L5 = tk.Label(L5_frame, bg='LightSalmon', font=('標楷體', 12), width=8, height=2)
L5.pack(side=tk.LEFT, padx=10, pady=5)

# 資料視覺化
plot_frame = tk.LabelFrame(window, text='檔案資料視覺化', font=('標楷體', 10), labelanchor='n')
plot_frame.pack(side=tk.TOP, padx=10, pady=5)
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
image_frame = tk.Frame(plot_frame)
image_frame.pack()
img = Image.open('plot.jpg')
img = ImageTk.PhotoImage(img)
showing = tk.Label(image_frame, image=img).pack(padx=30, pady=10)



window.mainloop()













