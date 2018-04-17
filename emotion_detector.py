import module_manager
module_manager.review()
import os
import random
import cv2
from shutil import copyfile
import numpy as np
import crop_face


#code adapted from Paul van Gent

emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy",
 "sadness", "surprise"]

face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt.xml')

#organises files

#reads a file
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

#gets all photos for a path
def getAllPhotos(path):
    if not os.path.isdir(path):
        return [path]
    else:
        allPhotos = []
        for filename in os.listdir(path):
            if filename != '.DS_Store':
                allPhotos.extend(getAllPhotos(path + '/' + filename))
        return allPhotos

#resizes all photos
def cropFaces(imageName):
    img = cv2.imread(imageName) #loads photo
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #converts to grayscale
    #detects the faces
    facesDetected = face_cascade.detectMultiScale(grayImg, 1.1, 5)
    if len(facesDetected) == 0: #checks if no face detected
        return ('No face detected, please try again')
    x,y,width,height = findLargestFace(facesDetected) #finds largest face
    #crops image based on rectangle of face
    cv2.rectangle(img,(x,y),(x+width+50,y+height+50),(255,255,255),2)
    croppedImage = img[y:y+height+50, x:x+width+50]
    croppedImage = cv2.resize(croppedImage,(350,350))
    #saves photo 
    name = imageName
    cv2.imwrite(name,croppedImage)


#maps participant number to all its useful Photos
def participantPhotos(path): #path is photo folder
    partPhotos = {}
    for participant in os.listdir(path):
        # allPhotos = []
        # partNum = participant[-3:]
        if participant == '.DS_Store':
            continue
        for face in os.listdir(path + '/' + participant):
            partNum = participant[-3:] + face
            usefulPhotos = []
            if face == '.DS_Store':
                continue
            photoPath = path + '/' + participant + '/' + face
            facePhotos = getAllPhotos(photoPath)
            usefulPhotos.append(facePhotos[0])
            usefulPhotos.append(facePhotos[-1])
            partPhotos[partNum] = usefulPhotos
    return partPhotos

#gets the file in directories
def getFile(path):
    if not os.path.isdir(path):
        return path
    else:
        for filename in os.listdir(path):
            if filename != '.DS_Store':
                return getFile(path + '/' + filename)


#gets result for each face
def getResult(path):
    participantResults = {}
    for participant in os.listdir(path):
        if participant == '.DS_Store':
            continue
        newPath = path + '/' + participant
        for face in os.listdir(newPath):
            if face == '.DS_Store':
                continue
            try:
                partNum = participant[-3:] + face
                files = getFile(newPath)
                emotion = int((readFile(files).strip())[0])
                emotion = emotions[emotion]
                participantResults[partNum] = ['neutral', emotion]
            except:
                pass
    return participantResults 

#maps emotion to list of photos
def emotionPhotos(partPhotos,participantResults):
    emotionPhoto = {'neutral': [], 
                    'anger':[], 
                    'contempt':[],
                    'disgust':[],
                    'fear':[],
                    'happy':[],
                    'sadness':[],
                    'surprise':[]
                    }
    for participant in participantResults:
        for i in range(len(participantResults[participant])):
            emotion = participantResults[participant][i]
            photo = partPhotos[participant][i]
            emotionPhoto[emotion].append(photo)
    return emotionPhoto

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

def cropEmotionPhotos(emotionPhoto):
    for key in emotionPhoto:
        for photoName in emotionPhoto[key]:
            cropFaces(photoName)

#machine learning part

fisherFace = cv2.face.FisherFaceRecognizer_create()


def separateFiles(emotion,emotionPhoto):
    files = emotionPhoto[emotion]
    random.shuffle(files)
    training = files[:int(len(files)*0.8)]
    prediction = files[-int(len(files)*0.2):]
    return training, prediction
    
def makeSets():
    
    partPhotos = participantPhotos('cohn-kanade-images')
    participantResults = getResult('Emotion')
    emotionPhoto = emotionPhotos(partPhotos,participantResults)
    cropEmotionPhotos(emotionPhoto)
    
    trainingData = []
    trainingLabels = []
    predictionData = []
    predictionLabels = []
    
    for emotion in emotions:
        training, prediction = separateFiles(emotion,emotionPhoto)
        for item in training:
            image = cv2.imread(item)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            trainingData.append(gray)
            trainingLabels.append(emotions.index(emotion))
        
        for item in prediction:
            image = cv2.imread(item)
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            predictionData.append(gray)
            predictionLabels.append(emotions.index(emotion))
    
    return trainingData,trainingLabels, predictionData, predictionLabels

def runRecogniser():
    trainingData, trainingLabels, predictionData, predictionLabels = makeSets()
    print ('training fisher face classifier...')
    print ("size of training set is:", len(trainingLabels), "images")
    fisherFace.train(trainingData, np.asarray(trainingLabels))
    print ('predicting classification set')
    
    count = 0
    correct = 0
    incorrect = 0
    for image in predictionData:
        pred, conf = fisherFace.predict(image)
        if pred == predictionLabels[count]:
            correct += 1
            count += 1
        else:
            incorrect += 1
            count += 1
    return ((100*correct)/(correct +incorrect))
    
metascore = []
for i in range(0,10):
    correct = runRecogniser()
    print ('got', correct, 'percent correct!')
    metascore.append(correct)

print ('\n\nend score:', np.mean(metascore), 'percent correct')
        
    
    
        
    

