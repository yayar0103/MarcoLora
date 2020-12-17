# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 18:08:52 2020

@author: yayar
"""

import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
import numpy as np
from tkinter import filedialog
import matplotlib.pyplot as plt
import LoRa
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib as plt
plt.use("TkAgg")
style.use("classic")

window = tk.Tk()
window.title('Acoustic Software')
window.geometry('1500x900')

style01 = ttk.Style()
style01.theme_use("default")
style01.configure("Treeview", background='white', foreground='black', rowheight=25, fieldbackground='white')
style01.map('Treeview', background=[('selected', 'blue')])

running = False
index = 0
index_pil = 0

f1= Figure(figsize=(8, 8), dpi=60)
a = f1.add_subplot(111)
a.set_ylim(80,170)
a.set_xlim(0,30)
x150 = np.linspace(0, 30)
y150 = 150 + (0*x150)
a.plot(x150, y150, 'r-')

f2= Figure(figsize=(8, 8), dpi=60)
b = f2.add_subplot(111)
b.set_ylim(80,170)
b.set_xlim(0,30)

cursor = ''
connection = ''

xList = []
yList = []
xList02 = []
yList02 = []
recedB = []
receT = []
peak = 0

start_sec = 0
end_sec = 0

def connect():
    global running
    running = True
    global llora
    loraPort = str(llora_entry.get())
    llora = LoRa.LoRa(port=loraPort)
    a, b, c, d, e, f = llora.display_info()
    loraInfo = str(a +', '+ b +', ' + c +', '+ d +', '+ e +', '+ f)
    var02.set(loraInfo)
    print("loraInfo succesfully shown")
    llora.set_mode("rx")
    print("Set mode to RX")

def _insert(new_data): 
    global cursor
    global connection
    try:
        connection = mysql.connector.connect(host = 'localhost', database = 'lora', user = 'yayar', password = 'ntou414')
        sql = "INSERT INTO lora (time, dB) VALUES (%s, %s);"
        cursor = connection.cursor()
        cursor.execute(sql, new_data)
        connection.commit()
    except Error as e:
        print("資料庫連接失敗：", e)

def select_file01():
    file_path = filedialog.askopenfilename()
    var01.set(file_path)
    
def select_file30():
    file_path30 = filedialog.askopenfilename()
    var30.set(file_path30)

def rece_lora():
    global running
    global index
    global index_pil
    global input_pildB
    global llora
    global xList02
    global yList02
    global recedB
    global receT
    global peak
    global cursor
    global connection
    path = str(txt_entry.get())
    path30 = str(txt30_entry.get())
    if running == True:
        input_pildB = float(pildB_entry.get())
        input_overdB = float(overdB_entry.get())
        with open(path, "a") as s:
            received = llora.read()
            if received != None:
                print(received)
                timee = str(received.split("-")[0])
                dBB = str(received.split("-")[1])
                if float(dBB) >= input_overdB:
                    receData.insert("", index, values=(timee, dBB), tags=('redd', ))
                    print('Hey the number is over!')
                else:
                    receData.insert("", index, values=(timee, dBB))
                # _insert((timee, dBB))
                receT.append(timee)
                recedB.append(float(dBB))
                index -= 1
                s.write(str(received) + "\n")
                print("-------------------")
            if len(recedB) >= 30:
                with open(path30, "a") as s30:
                    
                    print("HIHIHIHIHIHIHIHIHIHIHIHIHI!")     
                    pilNum = 0
                    selEn = 0
                    sel30 = 0
                    for i in range(len(recedB)):
                        if (recedB[i] >= input_pildB):
                            pilNum += 1
                    recedB = np.array(recedB)
                    receT = np.array(receT)
                    selEn = np.sum(np.power(10, recedB/20))
                    sel_summ =selEn / pilNum
                    sel30 = round(20*np.log10(sel_summ), 1)
                    sel30Data.insert("", index_pil, values=(receT[0], str(sel30)))
                    s30.write(str(receT[0]) + "-" + str(sel30)+ "\n")
                    if peak < sel30:
                        peak = sel30
                        var_peak.set(peak)
                    recedB = []
                    receT = []
    window.after(300, rece_lora)
                       
def disconnect():
    global llora
    global running
    global cursor
    global connection
    running = False
    a = llora.close()
    var02.set(a)
    cursor.close()
    connection.close()
    
    
def delButton():
    global xList
    global yList
    x = receData.get_children()
    for item in x:
        receData.delete(item)
        
def animate(i):
    global running
    global xList
    global yList
    global x150
    global y150
    path = str(txt_entry.get())
    if running == True:
        input_overdB = float(overdB_entry.get())
        data = open(path, "r").read()
        dataList = data.split('\n')
        for each in dataList:
            if len(each)>1:
                x,y = each.split('-')
                if float(y) >= input_overdB:
                    window.configure(bg='red')
                else:
                    window.configure(bg='white')
                if len(xList)<10:
                    xList.append(str(x))
                    yList.append(float(y))
                else:
                    xList[0:9] = xList[1:10]
                    xList[9] = str(x)
                    yList[0:9] = yList[1:10]
                    yList[9] = float(y)
        a.clear()
        a.plot(x150, y150, 'r-')
        a.set_ylim(80,170)
        a.set_xlim(0,len(xList))
        a.plot(xList, yList, '--o')
        a.set_xticklabels(xList, rotation = 45)
        a.grid()
        
def animate30(i):
    global running
    global xList02
    global yList02
    path30 = str(txt30_entry.get())
    if running == True:
        data = open(path30, "r").read()
        dataList = data.split('\n')
        for each in dataList:
            if len(each)>1:
                x,y = each.split('-')
                if len(xList02)<10:
                    xList02.append(str(x))
                    yList02.append(float(y))
                else:
                    xList02[0:9] = xList02[1:10]
                    xList02[9] = str(x)
                    yList02[0:9] = yList02[1:10]
                    yList02[9] = float(y)
        b.clear()
        b.set_ylim(80,170)
        b.set_xlim(0,len(xList02))
        b.plot(xList02, yList02, '--o')
        b.set_xticklabels(xList02, rotation = 45)
        b.grid()
                

header_label = tk.Label(window, text='水下聲學即時監測系統', font=('標楷體', 40, 'bold'))
header_label.pack(padx=5, pady=20)

set_frame = tk.Frame(window)
set_frame.pack()

txt_frame = tk.LabelFrame(set_frame, text='接收資料前設定', font=('標楷體', 10), labelanchor='n')
txt_frame.pack(side=tk.LEFT, padx=20, pady=30)
cotc_frame = tk.Frame(txt_frame)
cotc_frame.pack()
txt_label = tk.Label(cotc_frame, text='儲存檔案路徑選取', font=('標楷體', 12))
txt_label.pack(side=tk.LEFT, padx=20, pady=10)
var01 = tk.StringVar()
txt_entry = tk.Entry(cotc_frame, textvariable=var01, bd = 5, font=('標楷體', 8), width=30)
txt_entry.pack(side=tk.LEFT, padx=5, pady=10)
txt_btn = tk.Button(cotc_frame, text='選取檔案', font=('標楷體', 12), command = select_file01)
txt_btn.pack(side=tk.LEFT, padx=15, pady=10)

txt30_label = tk.Label(cotc_frame, text='儲存SEL30檔案路徑選取', font=('標楷體', 12))
txt30_label.pack(side=tk.LEFT, padx=20, pady=10)
var30 = tk.StringVar()
txt30_entry = tk.Entry(cotc_frame, textvariable=var30, bd = 5, font=('標楷體', 8), width=30)
txt30_entry.pack(side=tk.LEFT, padx=5, pady=10)
txt30_btn = tk.Button(cotc_frame, text='選取檔案', font=('標楷體', 12), command = select_file30)
txt30_btn.pack(side=tk.LEFT, padx=15, pady=10)

data_frame = tk.Frame(txt_frame)
data_frame.pack(side=tk.TOP, pady=5)
pildB_text = tk.Label(data_frame, text='輸入界定為打樁的dB值', font=('標楷體', 12))
pildB_text.pack(side=tk.LEFT)
pildB_entry = tk.Entry(data_frame, bd = 5, font=('標楷體', 8), width=10)
pildB_entry.pack(side=tk.LEFT, padx=5)
overdB_text = tk.Label(data_frame, text='輸入界定為打樁超標的dB值', font=('標楷體', 12))
overdB_text.pack(side=tk.LEFT, padx=5)
overdB_entry = tk.Entry(data_frame, bd = 5, font=('標楷體', 8), width=10)
overdB_entry.pack(side=tk.LEFT, padx=5)
llora_text = tk.Label(data_frame, text='LoRa設備埠號', font=('標楷體', 12, 'bold'), fg='red')
llora_text.pack(side=tk.LEFT, padx=15)
llora_entry = tk.Entry(data_frame, bd = 5, font=('標楷體', 8), width=10)
llora_entry.pack(side=tk.LEFT)
lorabtn_frame = tk.Frame(txt_frame)
lorabtn_frame.pack()
connect_btn = tk.Button(lorabtn_frame, text='開啟接收功能', font=('標楷體', 12), command = connect)
connect_btn.pack(side=tk.LEFT, padx=5, pady=10)
disconnect_btn = tk.Button(lorabtn_frame, text='關閉接收功能', font=('標楷體', 12), command = disconnect)
disconnect_btn.pack(side=tk.LEFT)
var02 = tk.StringVar()
loraInfo = tk.Label(lorabtn_frame, bg='Khaki', textvariable=var02, font=('標楷體', 8), width=120, height=2)
loraInfo.pack(side=tk.LEFT, padx=10, pady=5)

recev_frame = tk.LabelFrame(window, text='均能音量(Leq) - 1秒一筆', font=('標楷體', 12, 'bold'), labelanchor='n')
recev_frame.pack(side=tk.LEFT, padx=15, pady=5)
delet_btn = tk.Button(recev_frame, text='清除所有資料', font=('標楷體', 12), command = delButton)
delet_btn.pack(side=tk.TOP, pady=10)
scrollBar = tk.Scrollbar(recev_frame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

receData = ttk.Treeview(recev_frame, height=25, show="headings", columns=("時間", "dB值"), style="mystyle.Treeview")
receData.column("時間", width=80, anchor='center') 
receData.column("dB值", width=50, anchor='center')
receData.heading("時間", text="時間") 
receData.heading("dB值", text="dB值")
receData.tag_configure('redd', background='pink')
receData.pack(side=tk.LEFT, padx=20, pady=15)
scrollBar.config(command=receData.yview)
canvas_frame = tk.Frame(recev_frame)
canvas_frame.pack(side=tk.RIGHT)
canvas = FigureCanvasTkAgg(f1, canvas_frame)
canvas.get_tk_widget().pack()
canvas.draw()
canvas._tkcanvas.pack(padx=10, pady=10)

pilFrame = tk.LabelFrame(window, text='聲音脈衝序列平均(SEL30) - 30秒一筆', font=('標楷體', 12, 'bold'), labelanchor='n')
pilFrame.pack(side=tk.LEFT, padx=15, pady=10)
peakFrame = tk.Frame(pilFrame)
peakFrame.pack()
delet30_btn = tk.Button(peakFrame, text='清除所有資料', font=('標楷體', 12), command = delButton)
delet30_btn.pack(side=tk.LEFT, padx=30, pady=10)
peak_lb = tk.Label(peakFrame, text='最大音壓位準(Lpeak)', font=('標楷體', 12, 'bold'))
peak_lb.pack(side=tk.LEFT, padx=5)
var_peak = tk.StringVar()
peakV = tk.Label(peakFrame, bg='Khaki', textvariable=var_peak, font=('標楷體', 12), width=10, height=2)
peakV.pack(side=tk.LEFT, padx=5, pady=5)
sel30Data = ttk.Treeview(pilFrame, height=25, show="headings", columns=("時間", "dB值"))
sel30Data.column("時間", width=80, anchor='center') 
sel30Data.column("dB值", width=50, anchor='center')
sel30Data.heading("時間", text="SEL時間") 
sel30Data.heading("dB值", text="dB值")
sel30Data.pack(side=tk.LEFT, padx=20, pady=15)
pil_frame = tk.Frame(pilFrame)
pil_frame.pack(side=tk.RIGHT)
canvas02 = FigureCanvasTkAgg(f2, pil_frame)
canvas02.get_tk_widget().pack()
canvas02.draw()
canvas02._tkcanvas.pack(padx=10, pady=10)

ani = animation.FuncAnimation(f1, animate, interval= 300) 
ani30 = animation.FuncAnimation(f2, animate30, interval= 300) 
window.after(300, rece_lora)
window.mainloop()

