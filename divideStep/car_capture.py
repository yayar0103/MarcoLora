import cv2
import numpy as np

cap = cv2.VideoCapture("D:/yayar/opencv/mp4video2/Rec3_20190925093105_S_1.mp4")
fgbg = cv2.createBackgroundSubtractorMOG2()   #影片分析，前景背景分離，凸顯移動物體類別
kernel = np.ones((11,11), np.uint8)


while(cap.isOpened()):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)     #backgroun 凸顯移動物體參數
    
    #二值化強調物件
    fgmask = cv2.GaussianBlur(fgmask,(5,5),0) #GaussianBlue
    ret,fgmask = cv2.threshold(fgmask,150,255,cv2.THRESH_BINARY)   #Threshold 物體色調變黑白
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel) #Morphological transformations-close 物體型態轉換
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
                              
    #影像背景轉換
    car = cv2.bitwise_and(frame,frame,mask = fgmask)  #get car real images
    car_mask = cv2.bitwise_not(fgmask)  #inverse car mask
  
    #物體加上邊框
    fagmaskcopy = fgmask.copy()
    car_contour1=frame.copy()
    contours, hierarchy = cv2.findContours( fagmaskcopy , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE )   
    car_contour1 = cv2.drawContours(car_contour1, contours, -1, (0,255,0), 3)  #draw car contour
    
    car_contour2=frame.copy()
    car_contour3=frame.copy()
    car_contour4=frame.copy()
    
    for i in range(len(contours)):
        cnt = contours[i]
        M = cv2.moments(cnt)         #取得輪廓中心
        area = cv2.contourArea(cnt)  #取得輪廓面積
     
        epsilon = 0.1*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        car_contour2 = cv2.drawContours(car_contour2, [approx], -1, (0,255,0), 3)  #draw car contour    

        hull = cv2.convexHull(cnt)
        car_contour3 = cv2.drawContours(car_contour3, [hull], -1, (0,255,0), 3)  #draw car contour    
        
        #矩形外框
        x,y,w,h = cv2.boundingRect(cnt)   #回傳矩形外框 xy:左上角座標 wh:寬高
        car_contour4 = cv2.rectangle(car_contour4,(x,y),(x+w,y+h),(0,255,0),2)
   
    cv2.imshow('fgmask',fgmask)
    cv2.imshow('car',car)
    cv2.imshow('frame', frame)
    #cv2.imshow('road_white',whiteroad_car)
    #cv2.imshow('car_contour1',car_contour1)
    #cv2.imshow('car_contour2',car_contour2)
    #cv2.imshow('car_contour3',car_contour3)
    #cv2.imshow('car_contour4',car_contour4)
    #cv2.imshow('carBoundary',carBoundary)
    k = cv2.waitKey(20) & 0xff
    if k == 27:    #案Esc 結束畫面
        break  
print("vedio not open")
cap.release()
cv2.destroyAllWindows()
    