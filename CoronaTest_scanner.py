import cv2
import numpy as np
from matplotlib import pyplot as plt
from tkinter import * 
import tkinter
import mysql.connector
from datetime import date
import time



my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="CoronaTestDB"
)
my_cursor = my_db.cursor()



Fenster = Tk()
Fenster.title ("Corona Test Scanner")
Fenster.geometry("300x300")

myvar = StringVar()

def mywarWritten(*args):
    print (myvar.get())

myvar.trace("w", mywarWritten)

text_entry = Entry(Fenster, textvariable=myvar)
text_entry.pack()

#def Eingabe():
#    print("Eingabe: %s" % (eingabeFeld.get()))
#    eingabeFeld.delete(0,END)
#    OpenCam()

def InDBSchreiben():
    my_cursor.execute("""INSERT INTO TESTS (USERID, DATUM, RESULTID) VALUES ('""" + StringVar(myvar) + """', '2021-11-22', '2');""")
    result = my_cursor.fetchall()
    for _ in result:
        print(_)

def OpenCam():
    if (ButtonOpenCam['state'] == tkinter.NORMAL):
        video = cv2.VideoCapture(0) 

        a = 0

        while True:
            a = a + 1
            check, frame = video.read()
            cv2.imshow("Capturing",frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        showPic = cv2.imwrite("filename.jpg",frame)
        print(showPic)

        video.release()
        cv2.destroyAllWindows 
        # Read image
        I = cv2.imread('filename.jpg',0)
        # Threshold
        IThresh = (I>=118).astype(np.uint8)*255
        # Remove from the image the biggest conneced componnet
        # Find the area of each connected component
        connectedComponentProps = cv2.connectedComponentsWithStats(IThresh, 8, cv2.CV_32S)

        IThreshOnlyInsideDrops = np.zeros_like(connectedComponentProps[1])
        IThreshOnlyInsideDrops = connectedComponentProps[1]
        stat = connectedComponentProps[2]
        maxArea = 0
        for label in range(connectedComponentProps[0]):
            cc = stat[label,:]
            if cc[cv2.CC_STAT_AREA] > maxArea:
                maxArea = cc[cv2.CC_STAT_AREA]
                maxIndex = label
        # Convert the background value to the foreground value
        for label in range(connectedComponentProps[0]):
            cc = stat[label,:]
        if cc[cv2.CC_STAT_AREA] == maxArea:
            IThreshOnlyInsideDrops[IThreshOnlyInsideDrops==label] = 0
        else:
            IThreshOnlyInsideDrops[IThreshOnlyInsideDrops == label] = 255
        # Fill in all the IThreshOnlyInsideDrops as 0 in original IThresh
        IThreshFill = IThresh
        IThreshFill[IThreshOnlyInsideDrops==255] = 0
        IThreshFill = np.logical_not(IThreshFill/255).astype(np.uint8)*255
        plt.imshow(IThreshFill)
        # Get numberof drops and cover precntage
        connectedComponentPropsFinal = cv2.connectedComponentsWithStats(IThreshFill, 8, cv2.CV_32S)
        NumberOfDrops = connectedComponentPropsFinal[0]

        print ("Number of drops = " + str(NumberOfDrops))

        time.sleep(6)
        
        cv2.destroyAllWindows()

        InDBSchreiben()


def Bestätigung():
    if (Button['state'] == tkinter.NORMAL):
        print ("Eingabe:"&myvar)




#eingabeFeld = Entry(Fenster)
#eingabeFeld.grid(row=5, column=1)
#Button(Fenster, text='Bestätigung', command=Bestätigung).grid(row=10, column=1, sticky=W, pady=5)

ButtonOpenCam = Button(master=Fenster, bg='white', text='Open Cam', command=OpenCam)
ButtonOpenCam.place(x=10, y=100, width=100, height=22)

exitButton = Button(master=Fenster, text='Schließen', command=Fenster.quit)
exitButton.place(x=5, y=275, width=80, height=22)





Fenster.mainloop()
mainloop()
