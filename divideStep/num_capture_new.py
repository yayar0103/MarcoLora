from PIL import Image
import pytesseract
import os


def numcapture(file):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    file_input = open('D:/yayar/opencv/time/timedect2.txt', mode = 'w')
    for v_index, file in enumerate(file):
        img = Image.open(file)
        text = pytesseract.image_to_string(img, lang='eng')
        print(text)
        #rint(v_index)
        file_input.write(text+'\n')
    file_input.close()

videofiles = []
num_path = os.path.abspath("D:/yayar/opencv/time")
print("現在目錄路徑:" + num_path)
for dirPath, dirNames, fileNames in sorted(os.walk(num_path)):
    print('dirPath', dirPath)
    print('dirNames', dirNames)
    print('fileNames', fileNames)
    print('---------------')
    for f in sorted(fileNames):
        inputFile = os.path.join(dirPath, f)
        print("inputFile:" + inputFile)
        lastFile = os.path.splitext(f)[-1]
        print("lastFile" + lastFile)
        print("---------------")
        if lastFile == ".jpg":
            videofiles.append(inputFile)
            
numcapture(videofiles)