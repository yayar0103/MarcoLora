import cv2
from darkflow.net.build import TFNet
import numpy as np
import pytesseract
import os


def playing(x):
    pass

# def tracking(file, vedio_index):
#     cap = cv2.VideoCapture(file)
#     cv2.namedWindow('car_contour3')
#     fps = cap.get(cv2.CAP_PROP_FRAME_COUNT)
#     loop_flag = 0
#     pos = 0
#     cv2.createTrackbar('play', 'car_contour3')
#     fgbg = cv2.createBackgroundSubtractorMOG2()
#     kernel = np.ones((11, 11), np.uint8)
#     time_num = 1
    
#     while(cap.isOpened()):
#         if loop_flag == pos:
#             loop_flag += 1
#             cv2.setTrackbarPos('play', 'car_contour3', loop_flag)
#         else:
#             pos = cv2.getTrackbarPos('play', 'car_contour3')
#             loop_flag = pos
#             cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
            
#         ret, frame = cap.read()
#         if frame is None:
#             vedio_index += 1
#             if vedio_index >= len(vediofiles):
#                 break
#             cap = cv2.VideoCapture(vediofiles[vedio_index])
#             ret, frame = cap.read()

def files_get_video(path):
    datafiles = []
    data_path = os.path.abspath(path)
    for dirPath, dirNames, fileNames in sorted(os.walk(data_path)):   
        for f in sorted(fileNames):
            inputFile = os.path.join(dirPath, f)
            lastFile = os.path.splitext(f)[-1]
            if lastFile == ".wav": 
                 datafiles.append(inputFile)
    return datafiles 
           
def open_video(path, mic_x):
    cap = cv2.VideoCapture(path)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) 
    
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('D:/yayar/opencv/mp4video2/project_two/output/Rec1.mp4',fourcc, 20.0, (int(width), int(height)))
    while(True):
        ret, frame = cap.read()                                      #開啟影片
        time = frame[0:30,385:640]                                   #擷取時間畫面位置
        cv2.line(frame, (mic_x, 0), (mic_x, 480), (0,0,255), 2)      #畫麥克風線 
    return cap, out, ret, frame, time

def yolo_detect(frame):          # yolo 辨識影片中物體
    options = {"model": "C:/Users/user/darkflow/cfg/yolo.cfg", "load": "C:/Users/user/darkflow/bin/yolov2.weights", "threshold": 0.1}
    tfnet = TFNet(options)
    results = tfnet.return_predict(frame)
    return results
   
def boxing(original_img, predictions):   #將辨識結果與影像結合
    newImage = np.copy(original_img)
    for result in predictions:
        top_x = result['topleft']['x']
        top_y = result['topleft']['y']
        btm_x = result['bottomright']['x']
        btm_y = result['bottomright']['y']
        confidence = result['confidence']
        label = result['label'] + " " + str(round(confidence, 3))
        if confidence > 0.3:
            newImage = cv2.rectangle(newImage, (top_x, top_y), (btm_x, btm_y), (255,0,0), 3)
            newImage = cv2.putText(newImage, label, (top_x, top_y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL , 0.8, (0, 230, 0), 1, cv2.LINE_AA)    
    return newImage

def time_cap(data, path):
    path_txt = path.split('.')[0] + ".txt"
    write_to = open(path_txt, mode='w')
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    text = pytesseract.image_to_string(data, lang='eng')
    write_to.write(text + '\n')

def train_cap(result, path):
    for i in result:        
        name = i['label']
        confidence = i['confidence']
        if name == 'train' and confidence > 0.3 :
            train_x1 = i['topleft']['x']
            train_x2 = i['bottomright']['x']
            cv2.imwrite('D:/yayar/opencv/mp4video2/project_two/photo/'+ str(test_num) + ".jpg", new_frame)
            if train_x1 < mic_x and train_x2 > mic_x:
                train_flag = 1
                time_cap(time, path)
                
if __name__ == "__main__":
    # 用 opencv 開啟影片
    path = r"D:\yayar\THESIS\VISUAL\mp4video2"
    mic_x=295
    vedios = files_get_video(path)
    for video in vedios:
        cap, out, ret, frame, time = open_video(video)
        if ret == True:                                   #true 影響開啟 false 影響開啟失敗
            frame = np.asarray(frame)
            result = yolo_detect(frame)                   #辨識後結果
            new_frame = boxing(frame, result)             #將辨識結果與影像結合
            train_cap(result, video)
            test_num = test_num +1
            
            out.write(new_frame)
            cv2.imshow('frame',new_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
