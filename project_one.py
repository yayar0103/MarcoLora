import cv2
import numpy as np
import os

def playing(x):
    pass

def carTracking(file,video_index):
    cap = cv2.VideoCapture(file)
    cv2.namedWindow('car_contour3')
    fps = cap.get(cv2.CAP_PROP_FPS) 
    fps_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    loop_flag = 0
    pos = 0
    cv2.createTrackbar('play', 'car_contour3', 0, fps_num, playing)
    fgbg = cv2.createBackgroundSubtractorMOG2()   #影片分析，前景背景分離，凸顯移動物體類別
    kernel = np.ones((11,11), np.uint8)
    time_num = 1

    while(cap.isOpened()):
        
        if loop_flag ==pos:
            loop_flag = loop_flag + 1
            cv2.setTrackbarPos('play', 'car_contour3', loop_flag)
        else:
            pos = cv2.getTrackbarPos("play", 'car_contour3')
            loop_flag = pos
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        
        ret, frame = cap.read()
        
        if frame is None:
            video_index += 1
            if video_index >= len(videofiles):
                break
            cap = cv2.VideoCapture(videofiles[ video_index ])
            ret, frame = cap.read()
        road=frame[295:385,0:440]
        time = frame[0:30,385:640]
    
        #二值化強調物件
        fgmask = fgbg.apply(road)    #backgroun 凸顯移動物體參數
        fgmask = cv2.GaussianBlur(fgmask,(5,5),0) #GaussianBlue
        ret,fgmask = cv2.threshold(fgmask,150,255,cv2.THRESH_BINARY)   #Threshold 物體色調變黑白
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel) #Morphological transformations-close 物體型態轉換
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
  
        #物體加上邊框
        contours, hierarchy = cv2.findContours( fgmask.copy() , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE )  
        car_contour1 = road.copy()
        car_contour1 = cv2.drawContours(car_contour1, contours, -1, (0,255,0), 3)  #draw car contour
    
        car_contour2=road.copy()
        car_contour3=road.copy()
        car_contour4=frame.copy()
        
        #設定車子進入範圍
        mic_x1=290
        mic_x2=300
        mic_y1=20
        mic_y2=70
        
        cv2.rectangle(car_contour3, (mic_x1, mic_y1), (mic_x2, mic_y2), (0,0,255), 2)   
        # cv2.rectangle(car_contour4, (mic_x1, mic_y1), (mic_x2, mic_y2), (0,0,255), 2)
        #畫面沒有車輛就清空poslist
        
        #對每一台車做處理
        for i in range(len(contours)):
            cnt = contours[i]
            #M = cv2.moments(cnt)         #取得輪廓中心
            #area = cv2.contourArea(cnt)  #取得輪廓面積
            x,y,w,h = cv2.boundingRect(cnt)    #回傳矩形外框 xy:左上角座標 wh:寬高
            
            epsilon = 0.1*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,epsilon,True)
            car_contour2 = cv2.drawContours(car_contour2, [approx], -1, (0,255,0), 3)  #draw car contour    

            hull = cv2.convexHull(cnt)
            car_contour3 = cv2.drawContours(car_contour3, [hull], -1, (200,150,100), 3)  #draw car contour
            car_contour4 = cv2.drawContours(car_contour4, [hull], -1, (200,150,100), 3)  #draw car contour
            if x < mic_x2 and x > mic_x1 and y < mic_y2:
                cv2.imwrite("time/" + str(time_num) + ".jpg", time )
                cv2.rectangle(time, (4, 5), (240, 30), (0,0,255), 5)   
                time_num = time_num + 1

    
    
                 
        cv2.imshow('time', time)
        # cv2.imshow('originalvideo', frame)
        #cv2.imshow('fgmask',fgmask)
        #cv2.imshow('car_contour1',car_contour1)
        #cv2.imshow('car_contour2',car_contour2)
        cv2.imshow('car_contour3',car_contour3)
        # cv2.imshow('car_contour4',car_contour4)
        #cv2.imshow('carBoundary',carBoundary)
        k = cv2.waitKey(20) & 0xff
        if k == 27:    #按Esc 結束畫面
            break  
    cap.release()
    cv2.destroyAllWindows()

video_index = 0
videofiles = []
cur_path = os.path.abspath("D:/yayar/opencv/mp4video2")
for dirPath, dirNames, fileNames in sorted(os.walk(cur_path)):
    print('dirPath', dirPath)
    print('dirNames', dirNames)
    print('fileNames', fileNames)
    print('---------------')
    for f in sorted(fileNames):
        inputFile = os.path.join(dirPath, f)
        lastFile = os.path.splitext(f)[-1]
        if lastFile == ".mp4":
            videofiles.append(inputFile)

carTracking(videofiles[0], video_index)

    