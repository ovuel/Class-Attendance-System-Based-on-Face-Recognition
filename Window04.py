# -*- coding: cp936 -*-
#test
#create a main page
import find_fac
import rm
import training
import pre
import sqlite3
import os
import cv2 as cv
import numpy as np
from Tkinter import*
import ttk
from PIL import Image,ImageTk
 #注意要大写
class myCamera:
    def __init__(self,num):
        self.num_of_pics=num

    def take_pics(self,interval):
        cap = cv.VideoCapture(0)
        cap.set(3,640)
        cap.set(4,480)
        cap.set(5,30)
        i=0
        current_frame=0
        lis_pic=[]
        while(cap.isOpened()):
            ret,frame = cap.read()
            f_img=frame
            if ret:           
                frame = cv.flip(frame, 1)
                frame=cv.rectangle(frame,(220,120),(420,360),(0,255,0),1)
                frame=cv.rectangle(frame,(240,150),(400,355),(0,0,255),1)
                
                cv.putText(frame,'Press P,pic_num:'+str(len(lis_pic)),(180,100),cv.FONT_HERSHEY_SIMPLEX,0.5,255,2)
                cv.imshow("frame", frame)
                f_img=cv.cvtColor(f_img,cv.COLOR_BGR2GRAY)
                if cv.waitKey(1)&0xFF==ord('p') and current_frame%interval==0:
                    lis_pic.append(f_img)
                    i+=1
                    if i==self.num_of_pics:
                        break
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
                current_frame+=1
            else:
                break
            

        cap.release()
        cv.destroyAllWindows()
        return lis_pic

def take_pictures(event):
    eye_cascade = cv.CascadeClassifier(r'./data/haarcascade_eye.xml')
    face_cascade=cv.CascadeClassifier(r'./data/haarcascade_frontalface_alt.xml')
    c=myCamera(16)
    global lis_pic
    global photoimg
    lis_pic=c.take_pics(5)
    if len(lis_pic)==16:
        for i in range(16):
            lis_pic[i]=lis_pic[i][150:355,240:400]
            lis_pic[i]=find_fac.find_faces(lis_pic[i],3,face_cascade)
            lis_pic[i]=pre.preprocess(lis_pic[i],1,eye_cascade)
            img=Image.fromarray(lis_pic[i])
            img=img.resize((100,100),Image.ANTIALIAS)
            photoimg[i]=ImageTk.PhotoImage(img)
            p[i]["image"]= photoimg[i]
    else:
        pass
        
def alter_pictures(event):
    eye_cascade = cv.CascadeClassifier(r'./data/haarcascade_eye.xml')
    face_cascade=cv.CascadeClassifier(r'./data/haarcascade_frontalface_alt.xml')
    global lis_pic,photoimg
    if len(lis_pic)==16:
        c=myCamera(1)
        pic=c.take_pics(1)
        if pic:
            for i in range(16):
                if i==int(event.widget["text"]):
                    lis_pic[i]=pic[0]
                    lis_pic[i]=lis_pic[i][150:355,240:400]
                    lis_pic[i]=find_fac.find_faces(lis_pic[i],3,face_cascade)
                    lis_pic[i]=pre.preprocess(lis_pic[i],1,eye_cascade)
                    img=Image.fromarray(lis_pic[i])
                    img=img.resize((100,100),Image.ANTIALIAS)
                    photoimg[i]=ImageTk.PhotoImage(img)
                    event.widget["image"]=photoimg[i]
                    break
        else:
            pass
    else:
        pass

def save_data(event):
    global lis_pic,photoimg
    if t2.get() and t1.get() and len(lis_pic)==16:
        Id=t2.get()
        db_path='./train/train_database/'+Id
        if os.path.exists(db_path):
            tL_show4=Toplevel(MainForm)
            tL_show4.wm_attributes("-topmost",1)
            tL_show4.title("Done!")
            t_label4=Label(tL_show4,text="This student/number has existed.")
            t_label4.pack()
        else:
            os.mkdir(db_path)
            for i in range(len(lis_pic)):
                img_path=db_path+'/'+str(i)+'.jpg'
                this_face=lis_pic[i]
                cv.imwrite(img_path,this_face)
            try:
                conn=sqlite3.connect("First.db")
                cur=conn.cursor()                   
                cur.execute('''Create Table If Not Exists Student(nums int,name text,pres boolean,times int,path text)''')
                cur.execute("insert into Student Values(%d,'%s',%d,%d,'%s')"%(int(Id),t1.get(),0,0,db_path))
                conn.commit()
            except:
                tL_show2=Toplevel(MainForm)
                tL_show2.wm_attributes("-topmost",1)
                tL_show2.title("Done!")
                t_label2=Label(tL_show2,text="Error in Database")
                t_label2.pack()
                
            finally:
                conn.close()
            
            t1.delete(0,END)
            t2.delete(0,END)
            lis_pic=[]
            photoimg=[]
            for j in p:
                j.image=None
            imageobj=np.zeros([64,48])
            imageobj=Image.fromarray(imageobj)
            for i in range(16):
                photoimg.append(ImageTk.PhotoImage(imageobj))
            print('save successfuly')
            
            tL_show=Toplevel(MainForm)
            tL_show.wm_attributes("-topmost",1)
            tL_show.title("Done!")
            t_label=Label(tL_show,text="save successfully!")
            t_label.pack()


def enroll_Page():
    if not os.path.exists('./train'):
            os.mkdir('./train')
    if not os.path.exists('./train/train_database'):
            os.mkdir('./train/train_database')
    global MainForm
    MainForm=Toplevel()
    MainForm.geometry("600x700")
    MainForm.title("Main page")
    imageobj=np.zeros([100,100])
    imageobj=Image.fromarray(imageobj)
    global photoimg,lis_pic,t1,t2
    photoimg=[]
    lis_pic=[]
    if len(photoimg)==0:
        for i in range(16):
            photoimg.append(ImageTk.PhotoImage(imageobj))
    else:
        pass
    f_show=Frame(MainForm,bd=1)
    f_show.pack(ipadx=53,ipady=3)
    frame_l=Frame(f_show)
    frame_l.pack(side="left")
    frame_r=Frame(f_show)
    frame_r.pack(fill=X)
    frame_b=Frame(MainForm)
    frame_b.pack(side="top",ipadx=3,ipady=3)
    l1=Label(frame_l,text="name:")
    l1.pack(pady=5)
    l2=Label(frame_l,text="ID:")
    l2.pack()
    t1=Entry(frame_r)
    t1.pack(side="top",pady=10) 
    t2=Entry(frame_r)
    t2.pack() 

    btn1=Button(frame_b,text="photo",fg="red")
    btn1.pack(side="left",padx=20)
    btn1.bind("<Button-1>",take_pictures)#事件类型，回调函数，‘’、‘+’=覆盖、添加

    btn2=Button(frame_b,text="save",fg="red")
    btn2.pack(side="left",padx=32)
    btn2.bind("<Button-1>",save_data)
    
    photo_frame=Frame(MainForm,bd=1)
    photo_frame.pack(side="top",pady=60)

    photo_frame1=Frame(photo_frame,bd=1)
    photo_frame1.pack(side="top")
    photo_frame2=Frame(photo_frame,bd=1)
    photo_frame2.pack(side="top")
    photo_frame3=Frame(photo_frame,bd=1)
    photo_frame3.pack(side="top")
    photo_frame4=Frame(photo_frame,bd=1)
    photo_frame4.pack(side="top")


    global p
    p=[]
    for i in range(16):
        if i<4:
            bt=Button(photo_frame1,text=str(i))
        elif i<8:
            bt=Button(photo_frame2,text=str(i))
        elif i<12:
            bt=Button(photo_frame3,text=str(i))
        else:
            bt=Button(photo_frame4,text=str(i))
        bt.pack(side="left")
        bt.bind("<Button-1>",alter_pictures)
        p.append(bt)





