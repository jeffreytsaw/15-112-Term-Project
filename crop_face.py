import numpy as np
import cv2
import glob

face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt.xml')

#finds largest face detected from list of faces detected
def findLargestFace(facesDetected):
    currMax = 0
    largestFace = None
    for face in facesDetected:
        #detected face given as x, y top left coords and width and height
        x,y,width,height = face
        if width*height > currMax:
            currmMax = width * height
            largestFace = (x,y,width,height)
    return largestFace

def cropFaces(imageName):
    img = cv2.imread(imageName) #loads photo
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #converts to grayscale
    #detects the faces
    facesDetected = face_cascade.detectMultiScale(grayImg, 1.1, 5)
    if len(facesDetected) == 0: #checks if no face detected
        return ('No face detected, please try again')
    x,y,width,height = findLargestFace(facesDetected) #finds largest face
    #crops image based on rectangle of face
    cv2.rectangle(img,(x,y),(x+width,y+height),(255,255,255),2)
    croppedImage = img[y:y+height, x:x+width]
    croppedImage = cv2.resize(croppedImage,(350,350))
    #saves photo 
    name = imageName
    cv2.imwrite(name,croppedImage)





# def cropFaces():
#     img = cv2.imread('photo.jpg') #loads photo
#     grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #converts to grayscale
#     #detects the faces
#     facesDetected = face_cascade.detectMultiScale(grayImg, 1.1, 5)
#     if len(facesDetected) == 0: #checks if no face detected
#         return ('No face detected, please try again')
#     x,y,width,height = findLargestFace(facesDetected) #finds largest face
#     #crops image based on rectangle of face
#     cv2.rectangle(img,(x,y),(x+width+50,y+height+50),(255,255,255),2)
#     croppedImage = img[y:y+height+50, x:x+width+50]
#     croppedImage = cv2.resize(croppedImage,(350,350))
#     #saves photo 
#     name = 'photo.jpg'
#     cv2.imwrite(name,croppedImage)
#     cv2.imshow('image',croppedImage)
#     cv2.waitKey(0)
# 
# cropFaces()

