import cv2 as cv
import mediapipe as mp
import time
import threading
import numpy as np
import os
from pydub import AudioSegment
import RPi.GPIO as GPIO
from pydub.playback import play

from pose_module import PoseDetector

home = os.getenv("HOME")
safe = home + "/Projek-K3/vision/utils/sound/aman.mpeg"
unsafe = home + "/Projek-K3/vision/utils/sound/tidak aman.mpeg"

def nothing():
    pass

def millis():
    return round(time.time()*1000)

def audio(action):
    safe_sound = AudioSegment.from_mp3(safe)
    unsafe_sound = AudioSegment.from_mp3(unsafe)

    if action == -1:
        pass
    elif action == 0:
        play(safe_sound)
        time.sleep(3)
    elif action == 1:
        play(unsafe_sound)
        time.sleep(3)

def buzzer(pin):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin,GPIO.OUT)

    GPIO.output(pin,GPIO.HIGH)
    print ("Beep")
    time.sleep(1.5) # Delay in seconds
    GPIO.output(pin,GPIO.LOW)
    print ("No Beep")
    time.sleep(1.5)



def main():
    path0 = home + "/Projek-K3/vision/utils/video/man walking.webm"
    path1 = home + "/Projek-K3/vision/utils/video/ivan manjat.MOV"
    path2 = home + "/Projek-K3/vision/utils/video/manjat kasur.webm"
    path3 = home + "/Projek-K3/vision/utils/video/manjat kursi.webm"
    path4 = home + "/Projek-K3/vision/utils/video/manjat kursi2.webm"
    path5 = home + "/Projek-K3/vision/utils/video/manjat kursi3.webm"
    path6 = home + "/Projek-K3/vision/utils/video/hasani manjat 2.webm"
    path7 = home + "/Projek-K3/vision/utils/video/hasani manjat 3.webm"
    path8 = home + "/Projek-K3/vision/utils/video/hasani manjat 4.webm"
    cap = cv.VideoCapture(path7)

    pd = PoseDetector()
    pTime = 0
    platform_status = False
    red = [0,0,255]
    window = "trackbar"

    pin = 23
    last_buzzer_call_time = 0
    buzzer_delay = 5

    action = -1
    i = 0

    cv.namedWindow(window)
    cv.createTrackbar('hue min',window,0,179,nothing)
    cv.createTrackbar('sat min',window,0,255,nothing)
    cv.createTrackbar('val min',window,0,255,nothing)
    
    cv.createTrackbar('hue max',window,0,179,nothing)
    cv.createTrackbar('sat max',window,0,255,nothing)
    cv.createTrackbar('val max',window,0,255,nothing)

    while cap.isOpened():
        grab, frame = cap.read()
        if not grab:
            print("capture failed")
            break

        dimension = (900,600)
        frame = cv.resize(frame,dimension,interpolation=cv.INTER_AREA)

        hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
        hmin = cv.getTrackbarPos('hue min',window)
        smin = cv.getTrackbarPos('sat min',window)
        vmin = cv.getTrackbarPos('val min',window)

        hmax = cv.getTrackbarPos('hue max',window)
        smax = cv.getTrackbarPos('sat max',window)
        vmax = cv.getTrackbarPos('val max',window)

        low = np.array([42,40,106])
        high = np.array([55,125,255])
        thresh = cv.inRange(hsv,low,high)
        cv.imshow(window,thresh)
        cv.putText(frame,"platform status: ",(30,50),cv.FONT_HERSHEY_PLAIN,3,red,3)

        drawing = frame.copy()
        contour = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)[0]
        for c in contour:
            area = cv.contourArea(c)
            cv.drawContours(drawing,[c],-1,red,3)
            if area > 4500 and area < 30000:
                # print(area)
                platform_status = True
        
        if platform_status == True:
            cv.putText(frame,"present",(450,50),cv.FONT_HERSHEY_PLAIN,3,red,3)
            print("platform present, please becareful!")
            action = 0

        elif platform_status == False:
            cv.putText(frame,"absent",(450,50),cv.FONT_HERSHEY_PLAIN,3,red,3)
            # cv.line(frame,(225,460),(675,460),[0,0,255],3)
            cv.line(frame,(225,400),(675,400),[0,0,255],3)

            frame = pd.findPose(frame)
            lmlist = pd.findPosition(frame,False)
            if len(lmlist) != 0:
                cv.circle(frame, (lmlist[27][1], lmlist[27][2]), 15, (0, 0, 255), cv.FILLED)
                cv.circle(frame, (lmlist[28][1], lmlist[28][2]), 15, (0, 0, 255), cv.FILLED)
                if lmlist[27][2] and lmlist[28][2] < 400:      #parameter tidak aman
                    print("WARNING: unsafe action!!!")
                    action = 1

        platform_status = False

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(frame,str(int(fps)),(800,50),cv.FONT_HERSHEY_PLAIN,3,(255, 0, 0),3)

        tAudio = threading.Thread(target=audio,args=(action,))
        # tBuzzer = threading.Thread(target=buzzer,args=(pin,))
        # tTime = threading.Timer(1,audio,[action])
        # tTime.start()
        print(action)
        i += 10
        print(i)
        # if action == 1: 
        #     # tAudio.start()
        #     tBuzzer.start()
        #     i = 0
            # time.sleep(1)
            
        if action == 1:
            current_time = time.time()
            if current_time - last_buzzer_call_time >= buzzer_delay:
                tBuzzer = threading.Thread(target=buzzer, args=(pin,))
                tBuzzer.start()
                last_buzzer_call_time = current_time

        # if i == 1000 and action != -1: 
        #     tAudio = threading.Thread(target=audio, args=(action,))
        #     tAudio.start()
        #     i = 0


        # print(i)
        # print(action)
        cv.imshow("video",frame)
        # cv.imshow("contour",drawing)
        cv.waitKey(30)
    
    action = -1


if __name__ == "__main__":
    main()