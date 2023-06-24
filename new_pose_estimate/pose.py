import cv2 as cv
import mediapipe as mp
from playsound import playsound
import time

path0 = "/home/kosmos/Videos/man walking.webm"
path1 = "/home/kosmos/Videos/ivan manjat.MOV"

cap = cv.VideoCapture(path1)

pTime = 0

mpPose = mp.solutions.pose
mpDraw = mp.solutions.drawing_utils
pose = mpPose.Pose()

while True:
    grab, frame = cap.read()

    if not grab:
        print("no video avaiable")

    frame = cv.resize(frame,(800,500))

    rgb = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    result = pose.process(rgb)
    # print(result.pose_landmarks)

    if result.pose_landmarks:
        mpDraw.draw_landmarks(frame,result.pose_landmarks,mpPose.POSE_CONNECTIONS)
        for id,lm in enumerate(result.pose_landmarks.landmark):
            h,w,c = frame.shape
            print(id,lm)
            px, py = int(lm.x * w), int(lm.y * h)
            cv.circle(frame,(px,py),3,(255,0,0),cv.FILLED)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(frame,str(int(fps)),(30,50),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv.imshow("video",frame)
    cv.waitKey(15)