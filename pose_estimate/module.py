import cv2 as cv
import mediapipe as mp
import time


class Detector:
    def __init__(self, static_image_mode = False, model_complexity = 0, smooth_landmarks = True, 
                 enable_segmetation = False,smooth_segmentation = False,
                 min_detection_confidence = 0.5, min_tracking_confidence = 0.5):
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmetation = enable_segmetation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        
        #setting mediapipe
        self.mp_pose = mp.solutions.mediapipe.python.solutions.pose
        self.mp_draw = mp.solutions.mediapipe.python.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(self.static_image_mode,self.model_complexity, self.smooth_landmarks,
                                      self.enable_segmetation, self.smooth_segmentation, self.min_detection_confidence,self.min_tracking_confidence)
        
    
    def find_pose(self, img, draw = True):
        #change image color format to rgb
        img_rgb = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        res = self.pose.process(img_rgb)         #get pose from video
        # print(res.pose_landmarks)         #print landmark pose
        if self.res.pose_landmarks:
            if draw:
                self.mp_draw.draw_landmarks(img,res.pose_landmarks,self.mp_pose.POSE_CONNECTIONS)
        return img
    

    # #resize video
    # width = 900
    # height = 600
    # img_size = (width,height)
    # img = cv.resize(img,img_size,interpolation=cv.INTER_AREA)
    
    
    # #change image color format to rgb
    # img_rgb = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    # res = pose.process(img_rgb)         #get pose from video
    # # print(res.pose_landmarks)         #print landmark pose
    
    # if res.pose_landmarks: 
    #     mp_draw.draw_landmarks(img,res.pose_landmarks,mp_pose.POSE_CONNECTIONS)         #draw pose
    #     for id, landmark, in enumerate(res.pose_landmarks.landmark):
    #         h_poseIm, w_poseIm, channel = img.shape
    #         print(id,landmark)      #print id and landmark
    #         pix_val_x, pix_val_y = int(landmark.x * w_poseIm), int(landmark.y * h_poseIm)
    #         cv.circle(img,(pix_val_x,pix_val_y),5,(255,0,0),2,cv.FILLED)
    #         # print(pix_val_x,pix_val_y)
    
    # cv.imshow("video",img)
    # cv.waitKey(10)
    
def main():
    cap = cv.VideoCapture(0)
    ptime = 0
    detector = Detector(False,False,True,0.5,0.5)
    
    while cap.isOpened():
        grab, frame = cap.read()
        if not grab:
            print("image not grabbed")
        
        detector.find_pose(frame)
        
        #get fps
        current_time = time.time()
        fps = 1/(current_time-ptime)
        ptime = current_time
        cv.putText(frame,str(int(fps)),(50,70),cv.FONT_HERSHEY_SIMPLEX,3,(0,0,255),3)
        
        #display video
        cv.imshow("video",frame)
        cv.waitKey(10)
    
    
# #if called run the main function
if __name__ == "__main__":
    main()