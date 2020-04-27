# MarcoLora
In ofshore ocean, Raspberrypi connect Hydrophones to detect underwater noise, after detecting processing the data and using lora to transport data to laptop

## Hardware
* GPS : [**L76 GPS HAT**](https://www.waveshare.com/wiki/L76X_GPS_HAT) by Waveshare
* Lora : [**LoRa USB dongle gateway**](http://www.ifroglab.com/tw/?p=7315) by iFrogLab 
* Hydrophone : [**icListen SC2**](https://oceansonics.com/products/iclisten-sc2/) by ocean sonics
## Install

```
pip install soundfile 
```
```
sudo apt-get install libsndfile1
```
#### Download folder main\ all files and import
```
import LoRa.py
import L76X.py
```

## Step of code
1.  Download the files which Hydrophone already output then save in raspberrypi.
2.  waiting for Hydrophone output tje next data in one minute.
3.  Get offical time and position from GPS.
4.  **Starting detect and download the file.**
5.  **Processing the file, using 1/3 octve filter output dB values in one second.**
6.  **Back up output datas in txt files in raspberrypi.**  
7.  **Use lora sent output datas.**
8.  (recycle 4.-8.)
