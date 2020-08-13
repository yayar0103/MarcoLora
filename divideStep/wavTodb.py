# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 20:33:27 2020

@author: yayar
"""
from scipy import signal
import wave
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import wavfile
import soundfile as sf
import scipy.io.wavfile as sciwave

def pysound_input(path, startF, endF):   #
    pysData, pysSr = sf.read(path, start = startF, stop = endF, dtype = 'int32')
    #x = np.linspace(1, 60, 63999)
    #plt.figure(figsize = (20,20))
    #plt.subplot(3,1,1)
    #plt.plot(x, pysData)
    #plt.title("pysound Data")
    return pysData

def wavfile_input(path, log=False):
    wavSr, wavData, dd = wavfile.read(path)
    plt.figure()
    plt.plot(wavData)
    plt.title("wavefile Data")
    plt.show()
    return wavData

def scipy_input(path):
    scipyRate, scipyData = sciwave.read(path)
    plt.figure()
    plt.plot(scipyData)
    plt.title("scipy Data")
    plt.show()
    return scipyData

def librosa_input(path, samr):
    librosaData, librosaSr = librosa.load(path, samr)
    plt.figure()
    # librosa.display.waveplot(data, sr)
    plt.plot(librosaData)
    plt.title("librosa Data")
    plt.show()
    return librosaData

def wav_info(path):
    f = wave.open(path,"rb")
    nchannels, sampwidth, framerate, nframes, comptype, compname = f.getparams()
    print('- input file config -')
    print('nchannels:', nchannels)
    print('sampwidth:', sampwidth)
    print('framerate:', framerate)
    print('nframes:', nframes)
    print('comptype:', comptype)
    print('compname:', compname)
    f.close()

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
        
        # w, h = signal.sosfreqz(sos, worN=20000)
        # hz = (samr * 0.5 / np.pi) * w
        # ampti = np.log10(abs(h))*20
        
        # plt.ylim(-90, 5)
        # plt.xlim(5, 30000)
        # plt.semilogx(hz, ampti, label=None)
        # plt.title("1/3-Octave-Band Filter")
        # plt.xlabel("Frequency(Hz)")
        # plt.ylabel("Magnitude(dB)")
        
        # plt.plot(filteredData)
        # plt.title("Filtered Output Data (amplitude)")
        value = ((np.sum(filteredData**2)/31)**0.5)/presureStan
        rmsData.append(value)
    return rmsData

def data_dB(rmsdata, cnt):
    centerFeq = ['16', '20', '25', '31.5', '40', '50', '63', '80', '100', '125', '160', '200', '250', '315', '400', '500', '630', '800',
                          '1k', '1.25k', '1.6k', '2k', '2.5k', '3.15k', '4k', '5k', '6.3k', '8k', '10k', '12.5k', '16k']
    dbData = 20*np.log10(rms_data)
    #plt.subplot(3,1,(2,3))
    #plt.bar(centerFeq, dbData)
    #plt.title("Filtered Output Data (dB)")
    #plt.savefig(str(cnt) + ".png")
    return dbData

def data_spl(dbdata):
    dbdata_float = dbdata/10
    exp_data = []
    for i in dbdata_float:
        exp_data.append(10**i)
    dB = 10*np.log10(np.sum(exp_data))
    return dB
 
if __name__ == "__main__":
    datapath = r"D:\yayar\THESIS\MARCO\data\SCW1924_20200309_023901.wav" 
    audioInfo = sf.info(datapath)
    print(audioInfo)
    samplerate = audioInfo.samplerate  #64000
    frames = audioInfo.frames          #3776000
    counter = 1
    spl_data = []
    for start_frames in range(1, 3712002, samplerate):  #1~3712001, 64000
        end_frames = start_frames + samplerate - 1           #63999
        print("The " + str(counter) + "s data!")
        pysound_data = pysound_input(datapath, start_frames, end_frames)
        pysound_data = pysound_data/(2**23 - 1)/256
        
        # wavfile_data = wavfile_input(datapath)
        # wavfile_data = wavfile_data/(2**23 - 1)
        
        # scipy_data = scipy_input(datapath)
        # scipy_data = scipy_data/(2**7 - 1)
        
        # librosa_data = librosa_input(datapath, samplerate)
        # librosa_data = librosa_data*(2**23-1)
        
        rms_data = octave_filtered(pysound_data , samplerate)
        dB_data = data_dB(rms_data, counter)
        spl_data.append(data_spl(dB_data))
        counter += 1
    x = np.linspace(1, 59, 59) 
    plt.figure(figsize = (50,20))
    plt.bar(x, spl_data)
    plt.savefig("023901.png")
    plt.show()
    
   



