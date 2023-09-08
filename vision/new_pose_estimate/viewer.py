import cv2 as cv
import os

home = os.getenv("HOME")
# print(os.getenv("HOME"))
path = "/home/test/Projek-K3/vision/utils/video/hasani manjat 3.webm"

cap = cv.VideoCapture(path)

while cap.isOpened():
    grab,img = cap.read()
    
    if not grab:
        print("no image captured")

    cv.imshow("video",img)
    cv.waitKey(3)