# -*- coding: cp936 -*-
#test
#create a main page
import kaoqin2
import manager03
import Window04
from Tkinter import*
 #注意要大写
def kaoqin(event):
    kaoqin2.check_Page()
def database(event):
    manager03.db_Page()
def enroll(event):
    Window04.enroll_Page()
    
MainUI=Tk()
MainUI.geometry("200x300")
MainUI.title("Main page")
MainUI['background']='LightSlateGray'

B1=Button(MainUI,text='Check-in')
B1.pack(pady=20)
B1.bind("<Button-1>",kaoqin)

B2=Button(MainUI,text='Database')
B2.pack()
B2.bind("<Button-1>",database)

B3=Button(MainUI,text='Enroll')
B3.pack(pady=20)
B3.bind("<Button-1>",enroll)

MainUI.mainloop()

