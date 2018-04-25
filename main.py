# Updated Animation Starter Code

from tkinter import *
import time
from take_image import takeImage
from crop_face import cropFaces
from emotion_detector import *
from song_player import *


def init(data):
    data.mode = 'startScreen'
    data.startPhotos = ['Start_screen/angry1.gif','Start_screen/happy2.gif',
    'Start_screen/sad1.gif']
    data.index = 0
    data.currentPhoto = PhotoImage(file = data.startPhotos[data.index])
    data.timerCalls = 0
    data.emotion = None
    data.currTrack = None
    data.tracks = []
    data.duration = 0
    data.index = 0
    data.nextTrack = None
    
def mousePressed(event,data):
    if data.mode == 'startScreen': startScreenMousePressed(event,data)
    elif data.mode == 'playSong': playSongMousePressed(event,data)
    elif data.mode == 'helpScreen': helpScreenMousePressed(event,data)

def keyPressed(event, data):
    pass

def timerFired(data):
    if data.mode == 'startScreen':startScreenTimerFired(data)
    elif data.mode == 'playSong': playSongTimerFired(data)

def redrawAll(canvas, data):
    if data.mode == 'startScreen': startScreenRedrawAll(canvas,data)
    elif data.mode == 'playSong': playSongRedrawAll(canvas,data)
    elif data.mode == 'helpScreen': helpScreenRedrawAll(canvas,data)


def startScreenMousePressed(event,data):
    if ((data.width/2) - 100 <= event.x <=data.width/2 + 100 and 
    (data.height/2 + 60) -25 <= event.y <= (data.height/2 +60) + 25):
        takeImage()
        cropFaces('photo.jpg')
        try:
            data.emotion = predictEmotion()
        except:
            trainClassifier()
            data.emotion = predictEmotion()
        data.tracks = getTracks(data.emotion)
        data.mode = 'playSong'
        data.timerCalls = 0
    elif (data.width/2-100 <= event.x <=data.width/2 + 100 and 
    data.height/2 + 130 -25 <= event.y <=data.height/2 + 130 + 25):
        data.mode = 'helpScreen'
        
def startScreenKeyPressed(event, data):
    pass

def startScreenRedrawAll(canvas, data):
    canvas.create_image(data.width/2,data.height/2,image = data.currentPhoto)
    canvas.create_rectangle((data.width/2) - 100,(data.height/2 + 60) -25,
    data.width/2 + 100, (data.height/2 +60) + 25, width = 3, fill = 'yellow')
    canvas.create_text(data.width/2,data.height/2+60, 
    text = 'Click here to Start!', font = 'Arial 23')
    canvas.create_rectangle(data.width/2-100, data.height/2 + 130 -25, 
    data.width/2 + 100, data.height/2 + 130 + 25, width = 3, fill = 'yellow')
    canvas.create_text(data.width/2,data.height/2 + 130, text = 'Instructions', 
    font = 'Arial 23')
    canvas.create_text(data.width/2,data.height/2-60, 
    text = 'The Empathetic Jukebox', font = 'Arial 55 bold')
    

def startScreenTimerFired(data):
    data.timerCalls += 1
    if data.timerCalls % 10 == 0:
        data.index = (data.index + 1) % (len(data.startPhotos))
        data.currentPhoto = PhotoImage(file = data.startPhotos[data.index])
        

def helpScreenRedrawAll(canvas,data):
    helpText = ''' Welcome to The Empathetic Jukebox, the music player that tailors \n its music to the way YOU feel! To get started, simply go back to the \n main menu, and click on the 'Click here to Start!' button. Then, \n whenever you're ready, press the spacebar on your laptop to start \n playing music. The music player will automatically open a youtube \n page with the song. If you don't like the song, simply press the next \n song button, or if you would like to re-analyze your emotion, go \n ahead and press that button.
    '''
    canvas.create_text(data.width/2,100, text = 'Instructions:', 
    font = 'Arial 55 bold')
    canvas.create_text(0,300, text = helpText, 
    font = 'Helvetica 23', anchor = W)
    canvas.create_text(data.width/2,475,text = 'Enjoy! :)', 
    font = 'Helvetica 40 bold')
    canvas.create_rectangle(data.width/2 - 100, data.height/2 + 215 - 25,
    data.width/2 + 100, data.height/2 + 215 + 25, width = 3, fill = 'yellow')
    canvas.create_text(data.width/2, data.height/2 + 215, text = 'Main Menu',
    font = 'Arial 23')

def helpScreenMousePressed(event,data):
    if (data.width/2 - 100 <= event.x <= data.width/2 + 100 and
    data.height/2 + 215 - 25 <= event.y <= data.height/2 + 215 + 25):
        data.mode = 'startScreen'
    

def playSongMousePressed(event,data):
    if (data.width/2 + 150 - 100 <= event.x <= data.width/2+150+100 and 
        data.height/2 + 185 - 25 <= event.y <= data.height/2 + 185 + 25):
            data.timerCalls = (data.duration//3) - 1
    elif (data.width/2 - 150 - 100 <= event.x <= data.width/2-150+100 and 
        data.height/2 + 185 - 25 <= event.y <= data.height/2 + 185 + 25):
        takeImage()
        cropFaces('photo.jpg')
        try:
            data.emotion = predictEmotion()
        except:
            trainClassifier()
            data.emotion = predictEmotion()
        data.tracks = getTracks(data.emotion)
        data.mode = 'playSong'
        data.timerCalls = 0
    elif (data.width/2-100 <= event.x <= data.width/2+100 and
    data.height/2 + 270 - 25 <= event.y <= data.height/2 + 270 + 25):
        data.mode = 'startScreen'

def playSongKeyPressed(event,data):
    pass

def playSongRedrawAll(canvas,data):
    canvas.create_text(data.width/2,data.height/2-80,
    text = "You're feeling %s" %(data.emotion), font = 'Arial 55 bold')
    data.tracks = getTracks(data.emotion)
    canvas.create_text(data.width/2,data.height/2,
    text = "Playing %s songs..." %(data.emotion), font = 'Arial 30')
    if data.currTrack != None:
        canvas.create_text(data.width/2,data.height/2 + 80,
        text = "currently playing: %s" %(data.currTrack), font = 'Arial 20')
    canvas.create_rectangle(data.width/2 + 150 - 100, data.height/2 + 185 - 25,
    data.width/2+150+100,data.height/2 + 185+25,width = 3)
    canvas.create_text(data.width/2 + 150, data.height/2 + 185, 
    text = 'Next song: %s' %(data.nextTrack),font = 'Helvetica 15')
    canvas.create_rectangle(data.width/2 - 150 - 100, data.height/2 + 185 - 25,
    data.width/2-150+100,data.height/2 + 185+25,width = 3)
    canvas.create_text(data.width/2 - 150, data.height/2 + 185, 
    text = 'Re-analyze Emotion',font = 'Helvetica 15')
    canvas.create_rectangle(data.width/2-100,data.height/2 + 270 - 25,
    data.width/2+100,data.height/2 + 270+25,width = 3)
    canvas.create_text(data.width/2,data.height/2 + 270,text = 'Main Menu',
    font = 'Arial 23')
    

def playSongTimerFired(data):
    data.timerCalls += 1
    if data.timerCalls == 1:
        if data.tracks != []:
            if data.currTrack == None: 
                data.currTrack = data.tracks[data.index]
            else:
                data.currTrack = data.nextTrack
            data.duration = getDuration(data.currTrack) + 8 #adds offset
            print (data.index)
            url = getURL(data.currTrack)
            webbrowser.open(url)
            if data.index < len(data.tracks):
                data.index += 1
                if data.index < len(data.tracks)-1:
                    data.nextTrack = data.tracks[data.index + 1]
            
    if data.timerCalls == data.duration//3:
        data.timerCalls = 0
    # print (data.timerCalls)

def playSongKeyPressed(event,data):
    pass

    

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)  
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(700, 700)