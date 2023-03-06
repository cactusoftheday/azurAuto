import time
import cv2
import numpy as np
import mss
from matplotlib import pyplot as plt
import pyautogui
import mouse
from random import randrange
import tensorflow as tf
#need 2 taps and one confirm button to end battle
# Resizes an image and maintains aspect ratio

def screenshot():
    with mss.mss() as sct:
        monitor_number = 1
        mon = sct.monitors[monitor_number]

        # The screen part to capture
        monitor = {
            "top": mon["top"],  # 100px from the top
            "left": mon["left"],  # 100px from the left
            "width": mon["width"],
            "height": mon["height"],
            "mon": monitor_number,
        }
        #output = "sct-mon{mon}_{top}x{left}_{width}x{height}.png".format(**monitor)
        #mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

        return np.array(sct.grab(monitor))

def capture_image(np_img_rgb):
    img_gray = cv2.cvtColor(np_img_rgb,cv2.COLOR_BGR2GRAY)
    return img_gray

def randomClickInBox(obj): #obj is a list [(x1,y1),(x2,y2)] literally a box
    #frame = capture_image()
    #cv2.rectangle(frame, (obj[0],obj[1]), (obj[2], obj[3]), (255,0,0), 2)
    #(0,0) is the top left corner of the main display so if you have a second display, in my case 1920x1080, to the left of your main display than
    #my xDiff is -1920
    #Ex. the top left corner of my secondary display will be (-1920, 0)
    #yDiff exists if your laptop screens might be of different height such as my advertised 1920x1080 laptop is actually 1920x1270...
    xDiff = -1920 #change these so that the click may register properly on the emulator
    yDiff = 190
    randx = randrange(obj[0][0],obj[1][0]) + xDiff
    randy = randrange(obj[0][1],obj[1][1]) + yDiff
    print(randx, randy)
    mouse.move(randx,randy,True)
    mouse.click(button="left")
    #cv2.imwrite('res.png',frame)

def findEnemies(frame):
    enemyLocation = []
    template = cv2.imread('templates/LV snip.png', 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(frame,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.6 #60% threshold, could give false positives
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        enemyLocation.append([pt[0],pt[1], pt[0] + 50, pt[1] + 50])
        #cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

    #cv2.imshow('result',frame)
    '''for enemy in enemyLocation:
        print(enemy)'''
    #print(len(enemyLocation))
    return enemyLocation

def find(frame, templateName, thresholdVar):
    #should return an array
    loc = np.array([])
    threshold = thresholdVar
    template = cv2.imread('templates/' + templateName + '.png', 0)
    w, h = template.shape[::-1]
    while True:
        threshold -= 0.01
        #print("finding")
        res = cv2.matchTemplate(frame, template,cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        if(loc[0].size > 0 or threshold <= 0.6):
            break
    if(loc[0].size == 0):
        #did not find object
        print("did not find", templateName)
        return []
    for pt in zip(*loc[::-1]):
        print(pt)
    return [pt,w,h]

def click(templateName):
    img_rgb = screenshot()
    img_gray = capture_image(img_rgb)
    location = find(img_gray, templateName, 0.9)
    print(location)
    box = [location[0], (location[0][0] + location[1], location[0][1] + location[2])]
    #cv2.rectangle(img_rgb, box[0], box[1], (0, 0, 255), 2)
    #cv2.imwrite('res.png', img_rgb)
    randomClickInBox(box)

def tryClick(templateName):
    try:
        click(templateName)
        return True
    except:
        print(templateName + " could not be found")
        return False

def campaignAuto(counter, wait):
    time.sleep(3)
    while True:
        if(tryClick('go')):
            break
        time.sleep(2)
    time.sleep(5)
    while True:
        if(tryClick('go2')):
            break
        time.sleep(2)
    #long wait time
    waitTime = 14 #wait time is intially 14 seconds
    count = counter
    while count > 1:
        while True:
            time.sleep(waitTime)
            retire()
            if(tryClick('continue')):
                waitTime = wait
                break
            if(waitTime > 2):
                waitTime -= 1
        count -= 1
    #end function

def retire():#please set your desired quick retire options before running campaign auto
    if(not tryClick('sort')):
        print('no retiring at this time')
        return
    time.sleep(1)
    tryClick('quickRetire')
    time.sleep(1)
    tryClick('retireConfirm')
    time.sleep(1)
    randomClickInBox([(1249, 830),(1300,850)]) #testing some random click to continue from retirement
    time.sleep(1)
    randomClickInBox([(1249, 830),(1300,850)]) #testing some random click to continue from retirement
    time.sleep(1)
    tryClick('retireConfirm')
    time.sleep(1)
    tryClick('disassemble')
    time.sleep(1)
    randomClickInBox([(1249, 830),(1300,850)]) #testing some random click to continue from retirement
    time.sleep(1)
    tryClick('retireCancel')
    time.sleep(2)
    tryClick('autosearch')

if __name__ == "__main__":
    #sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))
    #print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
    #retire()
    #campaignAuto(3, 14) #hardmode auto
    #tryClick('autosearch')
    campaignAuto(10, 20) #fox mine auto
    #tryClick('continue')
