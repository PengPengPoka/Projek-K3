import cv2 as cv
import mediapipe as mp
from playsound import playsound
import time

class PoseDetector():
    def __init__(self, 
                 mode = False, 
                 complexity = 1, 
                 smooth = True, 
                 segmentation = False,
                 smoothSegmentation = True, 
                 detectCon = 0.5, 
                 trackCon = 0.5):
        
        self.static_image_mode = mode
        self.model_complexity = complexity
        self.smooth_landmarks = smooth
        self.enable_segmentation = segmentation
        self.smooth_segmentation = smoothSegmentation
        self.min_detection_confidence = detectCon
        self.min_tracking_confidence = trackCon

        self.mpPose = mp.solutions.mediapipe.solutions.pose
        self.mpDraw = mp.solutions.mediapipe.solutions.drawing_utils
        self.pose = self.mpPose.Pose(self.static_image_mode, 
                                     self.model_complexity, 
                                     self.smooth_landmarks, 
                                     self.enable_segmentation, 
                                     self.smooth_segmentation, 
                                     self.min_detection_confidence, 
                                     self.min_tracking_confidence)

    def findPose(self, img, draw = True):
        rgb = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.result = self.pose.process(rgb)
        if self.result.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.result.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        lm_list = []
        if self.result.pose_landmarks:
            for id,lm in enumerate(self.result.pose_landmarks.landmark):
                h,w,c = img.shape
                print(id,lm)
                px, py = int(lm.x * w), int(lm.y * h)
                lm_list.append([id,px,py])
                
                if draw:
                    cv.circle(img,(px,py),3,(255,0,0),cv.FILLED)

def main():
    path0 = "/home/kosmos/Videos/man walking.webm"
    path1 = "/home/kosmos/Videos/ivan manjat.MOV"

    detector = PoseDetector()

    cap = cv.VideoCapture(path1)
    pTime = 0

    while True:
        grab, frame = cap.read()

        if not grab:
            print("no video avaiable")

        frame = cv.resize(frame,(800,500))
        frame = detector.findPose(frame,True)
        LMlist = detector.findPosition(frame,True)
        print(LMlist)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(frame,str(int(fps)),(30,50),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

        cv.imshow("video",frame)
        cv.waitKey(3)
        

if __name__ == "__main__":
    main()