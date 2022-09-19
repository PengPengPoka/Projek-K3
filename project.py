from copyreg import constructor
import time
from tokenize import Double
import numpy as np
import mediapipe as mp
import cv2 as cv
from pose_module import poseDetector

def nothing():
    pass

video1 = '/home/kosmos/Videos/sample.mp4'
video2 = '/home/kosmos/Videos/Webcam/hasrob1.webm'
video3 = '/home/kosmos/Videos/Webcam/hasrob2.webm'

cap = cv.VideoCapture(video3)

ptime = 0
red = [0,0,255]
window = "trackbar"
isPlatformPresent = False

dp = poseDetector()

cv.namedWindow(window)
cv.createTrackbar('hue min',window,0,179,nothing)
cv.createTrackbar('sat min',window,4,255,nothing)
cv.createTrackbar('val min',window,197,255,nothing)
cv.createTrackbar('hue max',window,37,179,nothing)
cv.createTrackbar('sat max',window,20,255,nothing)
cv.createTrackbar('val max',window,255,255,nothing)

while cap.isOpened():
    grab, frame = cap.read()
    
    if not grab:
        print('image not grabbed!')
    
    # video scaling
    width = 900
    height = 600
    frame_dim = (width,height)
    frame = cv.resize(frame,frame_dim,interpolation=cv.INTER_AREA)
    
    blur = cv.GaussianBlur(frame,(5,5),0)
    
    frame_hsv = cv.cvtColor(blur,cv.COLOR_BGR2HSV)
    hmin = cv.getTrackbarPos('hue min',window)
    smin = cv.getTrackbarPos('sat min',window)
    vmin = cv.getTrackbarPos('val min',window)
    hmax = cv.getTrackbarPos('hue max',window)
    smax = cv.getTrackbarPos('sat max',window)
    vmax = cv.getTrackbarPos('val max',window)
    
    low = np.array([hmin,smin,vmin])
    high = np.array([hmax,smax,vmax])
    frame_mask = cv.inRange(frame_hsv,low,high)
    
    drawing = frame.copy()
    contour,hierarchy = cv.findContours(frame_mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    for i in contour:
        area = cv.contourArea(i)
        if area > 2000:
            # cv.drawContours(drawing,contour,-1,red,3,8)
            isPlatformPresent = True
            print(area)
    
    # frame_p = dp.findPose(frame)
    print(isPlatformPresent)
    # video fps
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv.putText(frame,str(int(fps)),(45,75),cv.FONT_HERSHEY_SIMPLEX,3,red,4)
    
    cv.imshow('video',frame)
    cv.imshow(window,frame_mask)
    cv.imshow('contour',drawing)
    # cv.imshow('blur',blur)
    # cv.imshow(window,frame_mask)
    # cv.imshow("")
    cv.waitKey(30)