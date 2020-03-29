import cv2
from darkflow.net.build import TFNet
import numpy as np


def boxing(original_img, predictions):
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

options = {"model": "C:/Users/user/darkflow/cfg/yolo.cfg", "load": "C:/Users/user/darkflow/bin/yolov2.weights", "threshold": 0.1}

tfnet = TFNet(options)

cap = cv2.VideoCapture('D:/yayar/opencv/mp4video2/Rec1.mp4')
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) 

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('D:/yayar/opencv/mp4video2/project_two/output/Rec1.mp4',fourcc, 20.0, (int(width), int(height)))

test_num = 1

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    road = frame[295:385,0:440]
    time = frame[0:30,385:640]
    
    mic_x=295
    
    cv2.line(road, (mic_x, 0), (mic_x, 480), (0,0,255), 2)    

    if ret == True:
        frame = np.asarray(frame)
        results = tfnet.return_predict(frame)
        new_frame = boxing(frame, results)
        
        for i in results:        
            name = i['label']
            confidence = i['confidence']
            if name == 'train' and confidence > 0.3 :
                print(str(test_num) +':' + name)
                train_x1 = i['topleft']['x']
                train_x2 = i['bottomright']['x']
                print(train_x1)
                cv2.imwrite('D:/yayar/opencv/mp4video2/project_two/photo/'+ str(test_num) + ".jpg", new_frame)
                    
                if train_x1 < mic_x and train_x2 > mic_x:
                    cv2.imwrite("D:/yayar/opencv/mp4video2/project_two/time/" + str(test_num) + ".jpg", time )
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
