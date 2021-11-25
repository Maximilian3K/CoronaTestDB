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


def ShowResults():
    my_cursor.execute("""SELECT * FROM RESULTS""")
    result = my_cursor.fetchall()  
    for _ in result:
        print(_)



Fenster = Tk()
Fenster.title ("Corona Test Scanner")
Fenster.geometry("900x300")

def OpenCam():
    if (ButtonOpenCam['state'] == tkinter.NORMAL):
        ShowResults()

ButtonOpenCam = Button(master=Fenster, bg='white', text='Vegan', command=OpenCam)
ButtonOpenCam.place(x=10, y=10, width=80, height=22)
exitButton = Button(master=Fenster, text='Schließen', command=Fenster.quit)
exitButton.place(x=5, y=275, width=80, height=22)

Fenster.mainloop()
mainloop()