from PIL import Image
import pytesseract
import os


def numcapture(write_to, file):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    img = Image.open(file)
    text = pytesseract.image_to_string(img, lang='eng')
    print(text)
    write_to.write(text + '\n')
    
    
videofiles = []
num_path = os.path.abspath("D:/yayar/opencv/mp4video2/project_3/time")
print("現在目錄路徑:" + num_path)
file_input = open('D:/yayar/opencv/mp4video2/project_3/time.txt', mode = 'w')
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
            
for k in videofiles:       
    numcapture(file_input, k)
    
file_input.close()
