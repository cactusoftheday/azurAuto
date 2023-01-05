import time

import numpy

from Enemy import Enemy
from fleet import fleet
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import pyautogui
import mouse
from random import randrange
import tensorflow as tf
#need 2 taps and one confirm button to end battle
# Resizes an image and maintains aspect ratio

def capture_image(img_rgb):
    img_gray = cv2.cvtColor(np.array(img_rgb),cv2.COLOR_BGR2GRAY)
    return img_gray

def randomClickInBox(obj): #obj is a list [(x1,y1),(x2,y2)] literally a box
    #frame = capture_image()
    #cv2.rectangle(frame, (obj[0],obj[1]), (obj[2], obj[3]), (255,0,0), 2)
    randx = randrange(obj[0][0],obj[1][0])
    randy = randrange(obj[0][1],obj[1][1])
    print(randx , randy)
    mouse.move(randx,randy,True)
    mouse.click(button="left")
    #cv2.imwrite('res.png',frame)
    #hi

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

def buttonLoc(frame): #current frame needs to be passed in as this should be in nearestEnemy and nearestEnemy needs the frame as well
    #must be careful in using this as moving to the enemy will also pop up the green locator
    #print("got here!")
    template = cv2.imread('templates/fleetLocator.png', 0)
    w, h = template.shape[::-1]
    buttonLoc = None
    threshold = 1.0
    loc = None
    res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    while loc[0].size == 0 and threshold >= 0.8:
        threshold -= 0.01
        #print("running")
        res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        #print(type(loc[0]))

    #print("got here!")
    buttonLoc = []
    for pt in zip(*loc[::-1]): #this should be the proper adjustment for the marker
        buttonLoc.append([pt[0]-25,pt[1]+225, pt[0] + 35, pt[1] + 250])
        #cv2.rectangle(frame, (pt[0]-15,pt[1]+225), (pt[0] + 35, pt[1] + 250), (0, 0, 255), 2)
    #print(len(buttonLoc))

    #cv2.imwrite('res.png', frame) #comment this line when not debugging

    return buttonLoc #may want to add the fleet's click box as a rectangle on to the image later on, could cause slower computation

def myFunc(enemy):
    return enemy.distance
def sortE(enemyDistanceList): #sort enemies by nearest to closest
    returnedList = sorted(enemyDistanceList, key = lambda enemy: enemy.distance) #sort by distance
    return returnedList

def orderEnemies(enemies, fleetLoc): #Order enemies by closest to farthest, enemies should also have an unreachable state
    #enemies are determined by how close they are by pythagorean theorem
    #print("hewwowo oworldwo!")
    enemyDistanceList = []
    fleetX = fleetLoc[0][0]
    fleetY = fleetLoc[0][1]
    template = cv2.imread('templates/LV snip.png', 0)
    w, h = template.shape[::-1]
    #print(enemies)
    for enemyCoord in enemies:
        #print(enemyCoord)
        enemyX = enemyCoord[0]
        enemyY = enemyCoord[1]
        coords = [enemyX,enemyY,enemyX+w,enemyY+h]
        #print(coords)
        tempDistance = math.dist([enemyX,enemyY],[fleetX,fleetY])
        enemyDistanceList.append(Enemy(tempDistance,coords))
    #print(enemyDistanceList)
    enemyDistanceList = sortE(enemyDistanceList)
    #print("successfully ordered enemies")
    #print(enemyDistanceList)
    return enemyDistanceList

def nearestEnemy(allEnemies, buttonLoc): #only returns enemies that can be reached
    enemyDistanceList = sortE(allEnemies)
    count = 0
    for enemy in enemyDistanceList:
        if(enemy.reachable):
            randomClickInBox(allEnemies[count]) #click closest and reachable enemy
            break
        count += 1

def moveFleet(frame): #moves fleet towards closest enemy if unreachable in that turn
    #this is too hard to think about so i'll do it later
    print("hewowowowowo worldowowo")

def find(frame, templateName, thresholdVar):
    #should return an array
    loc = np.array([])
    threshold = thresholdVar
    template = cv2.imread('templates/' + templateName + '.png', 0)
    w, h = template.shape[::-1]
    while True:
        threshold -= 0.01
        print("finding")
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


def findBoss(frame):
    bossLocation = []
    template = cv2.imread('templates/bossTemplate.png', 0)
    w, h = template.shape[::-1]
    threshold = 0.8  # 80% threshold, quite high but we can decrease from there
    loc = np.array([])
    print(type(loc))
    while True:
        threshold -= 0.01
        print("running")
        res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        print(loc)
        if (loc[0].size > 0 or threshold <= 0.8):
            break

    if(loc[0].size == 0):
        return False

    for pt in zip(*loc[::-1]):
        temp = []
        temp.append([pt[0], pt[1], pt[0] + 50, pt[1] + 50])
        # print(type(pt))
        bossLocation.append([pt[0], pt[1], pt[0] + 50, pt[1] + 50])
        #cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    #cv2.imshow('result', frame)
    return bossLocation

def switchFleet(frame):
    template = cv2.imread('templates/switch.png', 0)
    w, h = template.shape[::-1]
    threshold = 1.0
    loc = None
    res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    while loc[0].size == 0:
        threshold -= 0.01
        #print("running")
        res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        #print(type(loc[0]))

    #print("got here!")
    buttonLoc = []
    for pt in zip(*loc[::-1]):
        temp = []
        temp.append([pt[0], pt[1], pt[0] + w, pt[1] + h])  # this should be the proper adjustment for the marker
        buttonLoc.append(temp)
        #cv2.rectangle(frame, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    #print(len(buttonLoc))
    randomClickInBox(buttonLoc[0])

def combatModule():
    frame = capture_image()
    switchFleet(frame) #switches to mob fleet
    currentAmmoCount = 5
    while True:
        count = 0
        if(currentAmmoCount < 1):
            switchFleet(frame)
            currentAmmoCount = 5
        time.sleep(0.5)
        frame = capture_image()
        enemies = findEnemies(frame)
        #print(enemies)
        fleetLoc = buttonLoc(frame)
        #print(fleetLoc)
        enemyDistance = orderEnemies(enemies,fleetLoc)
        #print(enemyDistance)
        coord = findBoss(frame)
        while True:
            try:
                print("boss corrdinates:",coord)
                if(not coord):
                    raise Exception("boss not found")
                randomClickInBox(coord)
                input("Awaiting user to input")
                clickBattle(frame)
                while True:
                    frame = capture_image()
                    try:
                        continueFromBattleScreen(frame)
                        time.sleep(1)
                        break
                    except:
                        continue
                return True
            except:
                print("enemy coords",enemyDistance[count].coords)
                randomClickInBox(enemyDistance[count].coords)
                clickBattle(frame)
                currentAmmoCount -= 1
                time.sleep(12)
                break
            count += 1
        while True:
            frame = capture_image()
            try:
                continueFromBattleScreen(frame)
                time.sleep(1)

                break
            except:
                continue

def clickBattle(frame):
    buttonLoc = []
    template = cv2.imread('templates/LV snip.png', 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6  # 60% threshold, could give false positives
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        temp = []
        temp.append([pt[0], pt[1], pt[0] + 50, pt[1] + 50])
        # print(type(pt))
        buttonLoc.append(temp)
        #cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    #cv2.imshow('result', frame)
    '''for enemy in enemyLocation:
        print(enemy)'''
    try:
        randomClickInBox(buttonLoc[0])
    except:
        return False #could not find the button

def continueFromBattleScreen(frame):
    buttonLoc = []
    template = cv2.imread('templates/touchToContinue.png', 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6  # 60% threshold, could give false positives
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        temp = []
        temp.append([pt[0], pt[1], pt[0] + 50, pt[1] + 50])
        # print(type(pt))
        buttonLoc.append(temp)
        #cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    timeCount = 0.2
    randomClickInBox(buttonLoc[0])
    time.sleep(0.5)
    randomClickInBox(buttonLoc[0])  # gotta click twice
    buttonLoc = []
    template = cv2.imread('templates/confirmButton.png', 0)
    w, h = template.shape[::-1]
    while True:
        try:
            res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8  # 60% threshold, could give false positives
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                temp = []
                temp.append([pt[0], pt[1], pt[0] + w, pt[1] + h])
                # print(type(pt))
                buttonLoc.append(temp)
                #cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            randomClickInBox(buttonLoc[0])
            #cv2.imshow('result', frame)

            break
        except:
            time.sleep(timeCount)
            timeCount += 0.5
            if(timeCount >= 3):
                break

    buttonLoc = []
    template = cv2.imread('templates/confirmButton.png', 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.3  # 60% threshold, could give false positives
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        temp = []
        temp.append([pt[0], pt[1], pt[0] + w, pt[1] + h])
        # print(type(pt))
        buttonLoc.append(temp)
        #cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    time.sleep(1)
    randomClickInBox(buttonLoc[0])
    #cv2.imshow('result', frame)
    '''for enemy in buttonLoc:
        print(buttonLoc)'''

def scroll(direction,holdTime): #hold time is in seconds
    #should only take one second of scroll time to move around
    pyautogui.keyDown(direction)
    time.sleep(holdTime)
    pyautogui.keyUp(direction)

def click(templateName):
    img_rgb = cv2.cvtColor(numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    img_gray = capture_image(img_rgb)
    location = find(img_gray, templateName, 0.9)
    print(location)
    box = [location[0], (location[0][0] + location[1], location[0][1] + location[2])]
    cv2.rectangle(img_rgb, box[0], box[1], (0, 0, 255), 2)

    cv2.imwrite('res.png', img_rgb)
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
            if(tryClick('continue')):
                waitTime = wait
                break
            if(waitTime > 2):
                waitTime -= 1
        count -= 1
    #end function

if __name__ == "__main__":
    #sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))
    #print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
    time.sleep(1)
    campaignAuto(3, 14) #hardmode auto
    #tryClick('continue')

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
