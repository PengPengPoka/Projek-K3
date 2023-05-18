import cv2 as cv
import mediapipe as mp
import time    

def trackbar(win_nam,hmin,smin,vmin,
             hmax,smax,vmax):
    cv.namedWindow(win_nam)
    cv.createTrackbar("hue min",win_nam,hmin,179)
    cv.createTrackbar("sat min",win_nam,smin,255)
    cv.createTrackbar("val min",win_nam,vmin,255)
    cv.createTrackbar("hue max",win_nam,hmax,179)
    cv.createTrackbar("sat max",win_nam,smax,255)
    cv.createTrackbar("val max",win_nam,vmax,255)
    

video_path = '/home/kosmos/Videos/sample.mp4'
video_path2 = '/home/kosmos/Videos/Webcam/hasrob1.webm'
video_path3 = '/home/kosmos/Videos/Webcam/hasrob2.webm'
cap = cv.VideoCapture(0)

scale_percent = 50

#setting mediapipe
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

ptime = 0

object_present = False

hmin,smin,vmin = 0,0,0
hmax,smax,vmax = 179,255,255
scal_min = (hmin,smin,vmin)
scal_max = (hmax,smax,vmax)

while cap.isOpened():
    grab, img = cap.read()
    
    if not grab:
        print("image not grabbed")
    
    # resize video
    width = 900
    height = 600
    img_size = (width,height)
    img = cv.resize(img,img_size,interpolation=cv.INTER_AREA)
    
    #get fps
    current_time = time.time()
    fps = 1/(current_time-ptime)
    ptime = current_time
    cv.putText(img,str(int(fps)),(50,70),cv.FONT_HERSHEY_SIMPLEX,3,(0,0,255),3)
    
    #change image color format to rgb
    img_rgb = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    res = pose.process(img_rgb)         #get pose from video
    # print(res.pose_landmarks)         #print landmark pose
    
    # if res.pose_landmarks: 
    #     landmark_list = []
    #     mp_draw.draw_landmarks(img,res.pose_landmarks,mp_pose.POSE_CONNECTIONS)         #draw pose
    #     for id, landmark, in enumerate(res.pose_landmarks.landmark):
    #         h_poseIm, w_poseIm, channel = img.shape
    #         print(id,landmark)      #print id and landmark
    #         pix_val_x, pix_val_y = int(landmark.x * w_poseIm), int(landmark.y * h_poseIm)
    #         landmark_list.append([id,pix_val_x,pix_val_y])
    #         cv.circle(img,(pix_val_x,pix_val_y),5,(255,0,0),2,cv.FILLED)
    #         # print(id,pix_val_x,pix_val_y)
    
    cv.imshow("video",img)
    cv.waitKey(10)
    
    
    
    
    
    
