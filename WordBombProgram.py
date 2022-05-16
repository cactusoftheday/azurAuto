'''# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#import pytesseract

import cv2
import numpy as np
import PIL
from PIL import ImageGrab

#pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\kijij\\PycharmProjects\\Tesseract\\tesseract.exe'


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def captureImage():
    img = ImageGrab.grab(bbox=(900, 500, 1000, 600))  # x, y, w, h
    img = img.resize((400,400))
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

    return frame

def recognizeAndLabel():
    fun = 0
    change = []
    while fun < 8:
        frame = captureImage()
        boxes = pytesseract.image_to_boxes(frame)
        hImage, wImage = frame.shape
        for box in boxes.splitlines():
            box = box.split(' ')
            change.append(box[0])
            x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
            cv2.rectangle(frame, (x, hImage - y), (w, hImage - h), (0, 0, 255), 3)
            cv2.putText(frame, box[0], (x, hImage - y + 25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.imshow('result', frame)
        # fun = fun + 100
        if cv2.waitKey(1) & 0Xff == ord('q'):
            break
    for item in change:
        print(item, end=' ')
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See Py'''