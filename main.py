import time
import enemy, fleet
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import pyautogui
import mouse
from random import randrange
#need 2 taps and one confirm button to end battle
# Resizes an image and maintains aspect ratio

def capture_image():
    img_rgb = pyautogui.screenshot()
    img_gray = cv2.cvtColor(np.array(img_rgb),cv2.COLOR_BGR2GRAY)
    return img_gray

def randomClickInBox(obj): #obj is a list [x1,y1,x2,y2] literally a box
    print(obj)
    obj = obj[0]
    frame = capture_image()
    cv2.rectangle(frame, (obj[0],obj[1]), (obj[2], obj[3]), (255,0,0), 2)
    randx = randrange(obj[0],obj[2])
    randy = randrange(obj[1],obj[3])
    mouse.move(randx,randy,True)
    mouse.click(button="left")
    cv2.imwrite('res.png',frame)
    #hi

def findEnemies(frame):
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

def buttonLoc(frame): #current frame needs to be passed in as this should be in nearestEnemy and nearestEnemy needs the frame as well
    #must be careful in using this as moving to the enemy will also pop up the green locator
    print("got here!")
    template = cv2.imread('templates/fleetLocator.png', 0)
    w, h = template.shape[::-1]
    buttonLoc = None
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
    buttonLoc = []
    for pt in zip(*loc[::-1]):
        temp = []
        temp.append([pt[0]-25,pt[1]+225, pt[0] + 35, pt[1] + 250]) #this should be the proper adjustment for the marker
        buttonLoc.append(temp)
        cv2.rectangle(frame, (pt[0]-15,pt[1]+225), (pt[0] + 35, pt[1] + 250), (0, 0, 255), 2)
    print(len(buttonLoc))

    cv2.imwrite('res.png', frame) #comment this line when not debugging

    return buttonLoc #may want to add the fleet's click box as a rectangle on to the image later on, could cause slower computation

def myFunc(enemy):
    return enemy.distance
def sort(enemyDistanceList): #sort enemies by nearest to closest
    returnedList = sort(enemyDistanceList,key = myFunc)
    return returnedList

def orderEnemies(enemies, fleetLoc): #Order enemies by closest to farthest, enemies should also have an unreachable state
    #enemies are determined by how close they are by pythagorean theorem
    print("hewwowo oworldwo!")
    enemyDistanceList = []
    fleetX = fleetLoc[0]
    fleetY = fleetLoc[1]
    template = cv2.imread('templates/LV snip.png', 0)
    w, h = template.shape[::-1]
    for enemyCoord in enemies:
        enemyX = enemyCoord[0]
        enemyY = enemyCoord[1]
        coords = [enemyX,enemyY,enemyX+w,enemyY+h]
        tempDistance = math.dist([enemyX,enemyY],[fleetX,fleetY])
        tempEnemy = enemy(tempDistance,coords)
        enemyDistanceList.append(tempEnemy)
    enemyDistanceList = sort(enemyDistanceList)
    return enemyDistanceList

def nearestEnemy(allEnemies, buttonLoc): #only returns enemies that can be reached
    enemyDistanceList = sort(allEnemies)
    count = 0
    for enemy in enemyDistanceList:
        if(enemy.reachable):
            randomClickInBox(allEnemies[count]) #click closest and reachable enemy
            break
        count += 1

def moveFleet(frame): #moves fleet towards closest enemy if unreachable in that turn
    #this is too hard to think about so i'll do it later
    print("hewowowowowo worldowowo")

def findBoss(frame):
    bossLocation = []
    template = cv2.imread('templates/LV snip.png', 0)
    w, h = template.shape[::-1]
    threshold = 0.9  # 90% threshold, quite high but we can decrease from there
    while loc[0].size == 0 and threshold >= 0.6:
        threshold -= 0.01
        print("running")
        res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        print(type(loc[0]))

    if(loc[0].size == 0):
        return False

    for pt in zip(*loc[::-1]):
        temp = []
        temp.append([pt[0], pt[1], pt[0] + 50, pt[1] + 50])
        # print(type(pt))
        bossLocation.append(temp)
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    cv2.imshow('result', frame)
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
        cv2.rectangle(frame, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    print(len(buttonLoc))
    randomClickInBox(buttonLoc[0])

def combatModule():
    frame = capture_image()
    enemies = findEnemies(frame)
    fleetLoc = buttonLoc(frame)
    enemyDistance = orderEnemies(enemies,fleetLoc)
    count = 0
    while True:
        if(findBoss(frame) != False):
            randomClickInBox(findBoss(frame))
            clickBattle(frame)
            break
        if enemyDistance[count].reachable:
            randomClickInBox(enemyDistance[count].coords)
            clickBattle(frame)
            time.sleep(12)

            break
        count += 1

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
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    cv2.imshow('result', frame)
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
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
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
                cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            randomClickInBox(buttonLoc[0])
            cv2.imshow('result', frame)

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
    threshold = 0.8  # 60% threshold, could give false positives
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        temp = []
        temp.append([pt[0], pt[1], pt[0] + w, pt[1] + h])
        # print(type(pt))
        buttonLoc.append(temp)
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    time.sleep(1)
    randomClickInBox(buttonLoc[0])
    cv2.imshow('result', frame)
    '''for enemy in buttonLoc:
        print(buttonLoc)'''

def scroll(direction,holdTime): #hold time is in seconds
    #should only take one second of scroll time to move around
    pyautogui.keyDown(direction)
    time.sleep(holdTime)
    pyautogui.keyUp(direction)
print("Please bring up azur lane screen")
#time.sleep(5) #uncomment this when on a single monitor
frame = capture_image()
#buttonLoc(frame)
#clickBattle(frame)
continueFromBattleScreen(frame)

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
