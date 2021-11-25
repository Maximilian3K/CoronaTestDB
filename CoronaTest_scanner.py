import cv2
import numpy as np
from matplotlib import pyplot as plt
from tkinter import * 
import tkinter
import mysql.connector



my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="CoronaTestDB"
)
my_cursor = my_db.cursor()



Fenster = Tk()
Fenster.title ("Corona Test Scanner")
Fenster.geometry("900x300")



def executeDBcreate():
    my_cursor.execute("""DROP DATABASE IF EXISTS CoronaTestDB;
CREATE DATABASE IF NOT EXISTS CoronaTestDB;""")
    result = my_cursor.fetchall()  
    for _ in result:
        print(_)

def executeDBcreateTable():
    my_cursor.execute("""USE CoronaTestDB;

CREATE TABLE IF NOT EXISTS USER (
    USERID         INTEGER NOT NULL,
    VORNAME        VARCHAR(50),
    NACHNAME       VARCHAR(50),
PRIMARY KEY (USERID)
);

CREATE TABLE IF NOT EXISTS RESULTS (
    RESULTID       INTEGER NOT NULL,
    RESULTNAME     VARCHAR(50),
PRIMARY KEY (RESULTID)
);

CREATE TABLE IF NOT EXISTS TESTS (
    USERID         INTEGER NOT NULL,
    DATUM          DATE,
    RESULTID         INTEGER NOT NULL,
FOREIGN KEY (USERID)  REFERENCES USER (USERID),
FOREIGN KEY (RESULTID)  REFERENCES RESULTS (RESULTID)
);""")
    result = my_cursor.fetchall()  
    for _ in result:
        print(_)

def executeDBinsertData():
    my_cursor.execute("""USE CoronaTestDB;
INSERT INTO RESULTS (RESULTID, RESULTNAME) VALUES ('1', 'Negaiv');
INSERT INTO RESULTS (RESULTID, RESULTNAME) VALUES ('2', 'Positiv');
COMMIT WORK;""")
    result = my_cursor.fetchall()  
    for _ in result:
        print(_)

def InsertDatabse():
    if (ButtonInsertDatabase['state'] == tkinter.NORMAL):
        executeDBcreate(), executeDBcreateTable(), executeDBinsertData() 

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
        # Print
        print ("Number of drops = " + str(NumberOfDrops))



ButtonOpenCam = Button(master=Fenster, bg='white', text='Open Cam', command=OpenCam)
ButtonOpenCam.place(x=10, y=10, width=100, height=22)
ButtonInsertDatabase = Button(master=Fenster, bg='white', text='Insert DB', command=InsertDatabse)
ButtonInsertDatabase.place(x=120, y=10, width=100, height=22)
exitButton = Button(master=Fenster, text='Schließen', command=Fenster.quit)
exitButton.place(x=5, y=275, width=80, height=22)



Fenster.mainloop()
mainloop()