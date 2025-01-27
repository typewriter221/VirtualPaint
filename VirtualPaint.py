import cv2 as cv 
import numpy as np

shw = cv.imshow
frameWidth = 640
frameHeight = 480
print("Import Suceesfull")
cap = cv.VideoCapture(2)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150)
##BGO
myColors =[[76,130,86,152,255,255],
            [50,94,107,98,255,255],
            [0,106,140,24,255,255]]
myColorValues = [[235,52,0],
                 [52,235,180],
                 [52,158,235]]

points = [] #[x,y,colurID]
def findColor(img,myColors,myColorValues):
    imgHSV =cv.cvtColor(img,cv.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv.inRange(imgHSV,lower,upper)
        x,y = getContours(mask)
        cv.circle(imgResult,(x,y),10,myColorValues[count],cv.FILLED)
        #shw(str(color[0]),mask)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count +=1
    return newPoints
def getContours(img):
    contours, heirarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    x,y,w,h =0,0,0,0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area>500:
            #cv.drawContours(imgResult,cnt,-1,(255,0,0),3)
            peri = cv.arcLength(cnt,True)
            approx = cv.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv.boundingRect(approx)
    return x+w//2,y+h
            
def draw(points,myColorValues):
    for point in points:
        cv.circle(imgResult,(point[0],point[1]),10,myColorValues[point[2]],cv.FILLED)

while True:
    _, img = cap.read()
    imgResult = img.copy()
    #print(success)
    newPoints = findColor(img,myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            points.append(newP)
    if len(points)!=0:
        draw(points,myColorValues)
    shw("Output",imgResult)
    if cv.waitKey(100) & 0xFF == ord('q'):
        break
