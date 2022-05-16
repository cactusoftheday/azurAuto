import cv2
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pyautogui
#need 2 taps and one confirm button to end battle
# Resizes a image and maintains aspect ratio

def capture_image():
    img_rgb = pyautogui.screenshot()
    img_gray = cv.cvtColor(img_rgb,cv.COLOR_BGR2GRAY)
    return img_gray

img_rgb = cv.imread('testPhotos/4.png')
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread('templates/LV snip.png', 0)
w, h = template.shape[::-1]
res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
threshold = 0.6 #60% threshold, could give false positives
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
cv.imwrite('res.png',img_rgb)
print("Hello world!")
