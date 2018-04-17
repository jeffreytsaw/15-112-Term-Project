import numpy as np
import argparse
import cv2
import time

cap = cv2.VideoCapture(0)
cv2.namedWindow('untouched image')#creates window

def nothing(x):
    pass

while True:
    ret,frame = cap.read() #reads vid capture
    cv2.imshow('untouched image', frame) #displays window
    if not ret:
        break
    k = cv2.waitKey(1)
    if k % 256 == 32: 
        image = 'photo.jpg' 
        #saves image under above name if space pressed
        cv2.imwrite(image,frame)

cam.release()

cv2.destroyAllWindows()