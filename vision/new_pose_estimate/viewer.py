import cv2 as cv

cap = cv.VideoCapture(2)
cap2 = cv.VideoCapture(4)

while cap.isOpened():
    grab,img = cap.read()
    suc, img2 = cap2.read()
    
    if not grab:
        print("no image captured")
    else:
        cv.imshow("video",img)
        cv.imshow("video2",img2)
        cv.waitKey(3)