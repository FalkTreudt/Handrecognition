import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import numpy as np
import math
from time import sleep
from ctypes import cast, POINTER

#following libraries are for controlling windows sound:

#from comtypes import CLSCTX_ALL
#from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume

#library for creating xml file

import xml.etree.ElementTree as xml


##########
wCam, hCam = 640, 480
##########

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

#create handdetector and set detection confidence to 0.7

detector = htm.handDetector(detectionCon=0.7)

#create audio device for controlling the windows volume

#create Adui_device
#device = AudioUtilities.GetSpeakers()
#interface = device.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
#volume=cast(interface,POINTER(IAudioEndpointVolume))

#volume.GetMute()
#volume.GetMasterVolumeLevel()
#volRange = volume.GetVolumeRange()
#print(volRange[0],volRange[1])
#volume.SetMasterVolumeLevel(-20.0,None)

#define some test variable and some default values for windows_volume_contoll
#some of them arent used anymore and could be deleted
minVol= 0
maxVol = 179
ran=0
vol2=0

#Gereate XML File for ESP32 to read and controll Servos (Robotic Hand)

def GenerateXML(fileName,ran,ran2,ran3,ran4,ran5):
    #root=xml.Element("Fingers")
    
    #c1=xml.Element("Finger")
    #c2=xml.Element("Finger2")
    #c3=xml.Element("Finger3")
    #c4=xml.Element("Finger4")
    #c5=xml.Element("Finger5")
    
    #root.append(c1)
    #c1.text=str(ran)
    #root.append(c2)
    #c2.text=str(ran2)
    #root.append(c3)
    #c3.text=str(ran3)
    #root.append(c4)
    #c4.text=str(ran4)
    #root.append(c5)
    #c5.text=str(ran5)
    
    #tree=xml.ElementTree(root)

    #Open htdocs folder to save the created XML file so the ESP32 can connect to it later on

    #with open("C:\\Users\\falkt\\Desktop\\Server\\htdocs\\" + fileName,"wb") as files:
        #tree.write(files)
    sleep(0.002)

#always loop and measure range of fingers... should implement exception handling and a way to kill process, could be added later

while True:
    success, img = cap.read()
    detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList)!=0:
     #print(lmList[4],lmList[8])

     #paint skeleton an Picture to visualize the hand

     #Index
     x1, y1 = lmList[5][1], lmList[5][2]
     x2, y2 = lmList[8][1], lmList[8][2]
     
     #middle
     x3, y3 = lmList[9][1], lmList[9][2]
     x4, y4 = lmList[12][1], lmList[12][2]
     
     #ring
     x5, y5 = lmList[13][1], lmList[13][2]
     x6, y6 = lmList[16][1], lmList[16][2]
     
     #pinky
     x7, y7 = lmList[17][1], lmList[17][2]
     x8, y8 = lmList[20][1], lmList[20][2]
     
     #thumb
     x9, y9 = lmList[1][1], lmList[1][2]
     x10, y10 = lmList[4][1], lmList[4][2]
     
     #index
     cv2.circle(img,(x1,y1),15,(255,255,0))
     cv2.circle(img, (x2, y2), 15, (255, 255, 0))
     cv2.line(img,(x1,y1),(x2,y2),(255,255,0),3)
     cx,cy=(x1+x2)//2,(y1+y2)//2
     cv2.circle(img, (cx, cy), 15, (255, 255, 0))
     length = math.hypot(x2-x1,y2-y1)
     
     #middle
     cv2.circle(img,(x3,y3),15,(255,255,0))
     cv2.circle(img, (x4, y4), 15, (255, 255, 0))
     cv2.line(img,(x3,y3),(x4,y4),(255,255,0),3)
     cx2,cy2=(x3+x4)//2,(y3+y4)//2
     cv2.circle(img, (cx2, cy2), 15, (255, 255, 0))
     length2 = math.hypot(x4-x3,y4-y3)
     
     #ring
     cv2.circle(img,(x5,y5),15,(255,255,0))
     cv2.circle(img, (x6, y6), 15, (255, 255, 0))
     cv2.line(img,(x5,y5),(x6,y6),(255,255,0),3)
     cx3,cy3=(x5+x6)//2,(y5+y6)//2
     cv2.circle(img, (cx3, cy3), 15, (255, 255, 0))
     length3 = math.hypot(x6-x5,y6-y5)
     
     #pinky
     cv2.circle(img,(x7,y7),15,(255,255,0))
     cv2.circle(img, (x8, y8), 15, (255, 255, 0))
     cv2.line(img,(x7,y7),(x8,y8),(255,255,0),3)
     cx4,cy4=(x7+x8)//2,(y7+y8)//2
     cv2.circle(img, (cx4, cy4), 15, (255, 255, 0))
     length4 = math.hypot(x8-x7,y8-y7)
     
     #thumb
     cv2.circle(img,(x9,y9),15,(255,255,0))
     cv2.circle(img, (x10, y10), 15, (255, 255, 0))
     cv2.line(img,(x9,y9),(x10,y10),(255,255,0),3)
     cx5,cy5=(x9+x10)//2,(y9+y10)//2
     cv2.circle(img, (cx5, cy5), 15, (255, 255, 0))
     length5 = math.hypot(x10-x9,y10-y9)
     
     #print(length)

     #var name "vol" should be changed later (used in earlier versions to controll Windows volume...)

     vol = np.interp(length,[20,200],[minVol,maxVol])
     vol2= np.interp(length2,[20,200],[minVol,maxVol])
     vol3= np.interp(length3,[20,200],[minVol,maxVol])
     vol4= np.interp(length4,[20,200],[minVol,maxVol])
     vol5= np.interp(length5,[20,200],[minVol,maxVol])
     vol5 =vol5-30
     print("vol: ",vol,vol2,vol3,vol4,vol5)
     
     

     GenerateXML("Finger.xml",int(vol),int(vol2),int(vol3),int(vol4),int(vol5))

     #define Hand range and Volume Range to adjust the values so they fit for windows

     #Handrange from 70-300
     #Volume Range -96 0

     #vol = np.interp(length,[0,255],[minVol,maxVol])
     #print(vol)

     #finally set volume to measured range
     #volume.SetMasterVolumeLevel(vol, None)

     #visualize when the mesured distance is too short (could be used for binary switches)
     if length<70:
         cv2.circle(img, (cx, cy), 15, (0, 0, 255),cv2.FILLED)
        
    #measure time between frames to calculate FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime



    #print FPS just for testing, could be removed later
    cv2.putText(img,f"FPS: {int(fps)}",(40,50),cv2.FONT_HERSHEY_COMPLEX, 1,(255,0,0),3)

    cv2.imshow("Img",img)
    cv2.waitKey(1)
