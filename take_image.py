import numpy as np
import argparse
import cv2
import time

def nothing(x):
    pass
    
def takeImage():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('untouched image')#creates window
    while True:
        ret,frame = cap.read() #reads vid capture
        cv2.putText(frame,"Press Space to Start!", (250,700), cv2.FONT_HERSHEY_SIMPLEX, 2, 0)
        cv2.imshow('untouched image', frame) #displays window
        if not ret:
            break
        k = cv2.waitKey(1)
        if k % 256 == 32: 
            image = 'photo.jpg' 
            #saves image under above name if space pressed
            cv2.imwrite(image,frame)
            break
        elif k % 256 == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
