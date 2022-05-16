import cv2
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pyautogui
from random import randrange
#need 2 taps and one confirm button to end battle
# Resizes a image and maintains aspect ratio

def capture_image():
    img_rgb = pyautogui.screenshot()
    img_gray = cv.cvtColor(np.array(img_rgb),cv.COLOR_BGR2GRAY)
    return img_gray

def randomClickInBox(enemy): #enemy is a list [x1,y1,x2,y2]
    print("hello world!")
    randx = randrange(enemy[0],enemy[2])
    randy = randrange(enemy[1],enemy[3])
    pyautogui.moveTo(randx,randy)
    pyautogui.click()
    #hi

def mapScreenModule():
    frame = capture_image()
    enemyLocation = []
    template = cv.imread('templates/LV snip.png', 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(frame,template,cv.TM_CCOEFF_NORMED)
    threshold = 0.6 #60% threshold, could give false positives
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        temp = []
        temp.append(pt[0],pt[1], pt[0] + 50, pt[1] + 50)
        #print(type(pt))
        enemyLocation.append(temp)
        cv.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imshow('result',frame)
    for enemy in enemyLocation:
        print(enemy)
    if cv2.waitKey(1) & 0Xff == ord('q'):
        return


while True:
    mapScreenModule()
    if cv2.waitKey(1) & 0Xff == ord('q'):
        break

'''img_rgb = cv.imread('testPhotos/4.png')
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread('templates/LV snip.png', 0)
w, h = template.shape[::-1]
res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
threshold = 0.6 #60% threshold, could give false positives
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
cv.imwrite('res.png',img_rgb)'''
print("Hello world!")
