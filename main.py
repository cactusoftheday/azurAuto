import time
import cv2
import numpy as np
from matplotlib import pyplot as plt
import pyautogui
import mouse
from random import randrange
#need 2 taps and one confirm button to end battle
# Resizes a image and maintains aspect ratio

def capture_image():
    img_rgb = pyautogui.screenshot()
    img_gray = cv2.cvtColor(np.array(img_rgb),cv2.COLOR_BGR2GRAY)
    return img_gray

def randomClickInBox(enemy): #enemy is a list [x1,y1,x2,y2]
    print(enemy)
    enemy = enemy[0]
    frame = capture_image()
    cv2.rectangle(frame, (enemy[0],enemy[1]), (enemy[2], enemy[3]), (255,0,0), 2)
    randx = randrange(enemy[0],enemy[2])
    randy = randrange(enemy[1],enemy[3])
    mouse.move(randx,randy,True)
    mouse.click(button="left")
    cv2.imwrite('res.png',frame)
    #hi



def mapScreenModule():
    frame = capture_image()
    enemyLocation = []
    template = cv2.imread('templates/LV snip.png', 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(frame,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.6 #60% threshold, could give false positives
    loc = np.where( res >= threshold)

    for pt in zip(*loc[::-1]):
        temp = []
        temp.append([pt[0],pt[1], pt[0] + 50, pt[1] + 50])
        #print(type(pt))
        enemyLocation.append(temp)
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

    cv2.imshow('result',frame)
    '''for enemy in enemyLocation:
        print(enemy)'''
    print(len(enemyLocation))
    return enemyLocation

def fleetLocation(frame): #current frame needs to be passed in as this should be in nearestEnemy and nearestEnemy needs the frame as well
    #must be careful in using this as moving to the enemy will also pop up the green locator
    print("got here!")
    template = cv2.imread('templates/fleetLocator.png', 0)
    w, h = template.shape[::-1]
    fleetLocation = None
    threshold = 1.0
    loc = None
    res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    while loc[0].size == 0:
        threshold -= 0.01
        print("running")
        res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        print(type(loc[0]))

    print("got here!")
    fleetLocation = []
    for pt in zip(*loc[::-1]):
        temp = []
        temp.append([pt[0]-25,pt[1]+225, pt[0] + 35, pt[1] + 250]) #this should be the proper adjustment for the marker
        fleetLocation.append(temp)
        cv2.rectangle(frame, (pt[0]-15,pt[1]+225), (pt[0] + 35, pt[1] + 250), (0, 0, 255), 2)
    print(len(fleetLocation))

    cv2.imwrite('res.png', frame) #comment this line when not debugging

    return fleetLocation #may want to add the fleet's click box as a rectangle on to the image later on, could cause slower computation

def nearestEnemy(enemies, frame): #needs game screenshot (frame) as well
    print("hewwowo oworldwo!")
    fleetLocation
    fleetX = fleetLocation[0]
    fleetY = fleetLocation[1]
    for enemy in enemies:
        enemyX = enemy[0]
        enemyY = enemy[1]


print("Please bring up azur lane screen")
#time.sleep(5) #uncomment this when on a single monitor
frame = capture_image()
fleetLocation(frame)
print("done")
'''enemies = mapScreenModule()
randomClickInBox(enemies[0])'''


'''img_rgb = cv.imread('testPhotos/4.png')
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread('templates/LV snip.png', 0)
w, h = template.shape[::-1]
res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
threshold = 0.6 #60% threshold, could give false positives
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
cv.imwrite('res.png',img_rgb)


if cv2.waitKey(1) & 0Xff == ord('q'):
    return

'''
print("Hello world!")
