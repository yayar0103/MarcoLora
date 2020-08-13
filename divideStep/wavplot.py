# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:24:48 2020

@author: yayar
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import soundfile as sf

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
    plt.show()
    # plt.savefig(str(num) + "-1.jpg")
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
    plt.show()
    # plt.savefig(str(num) + "-2.jpg")
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
    plt.show()
    # plt.savefig(str(num) + "-3.jpg")

if __name__ == '__main__':
    path = r'D:\yayar\THESIS\REPORT\20200516\newdata\SCW1924_20200517_132643.wav'
    num = 132643
    sensity = -207.4
    fs, b = init(path, num) 
    # Sxx = spectrogram_(b, fs, sensity, num) 
    Pxx = sepctrum(b, fs, num)
    # octave(b, fs, sensity, num)     