# -*- coding: cp936 -*-
import os
import rm
import find_fac
import sqlite3
import face_matching
import data_collect
from Tkinter import *
import ttk
import cv2 as cv
from PIL import Image,ImageTk

class K_APP:
    def __init__(self, master):
        self.master = master
        self.initWidgets()
    def initWidgets(self):
        self.interval=2
        self.p_count=0
        self.shift_mark=1
        self.camera = cv.VideoCapture(0)    #摄像头
        self.L_camera=cv.VideoCapture(1)
        self.face_cascade=cv.CascadeClassifier(r'C:/Python27/Lib/site-packages/cv2/data/haarcascade_frontalface_alt.xml')
        self.on_off=False
        self.blur_set=1200
        self.threshold=75
        
        self.style=-1
        self.var=IntVar()
        c_style=Checkbutton(self.master,text="Take pictures automatically when faces are detected.",variable=self.var,onvalue=1,offvalue=0,command=self.changestyle)
        c_style.pack()

        self.panel = Label(self.master,width=640,height=480)  # initialize image panel
        self.panel.pack()

        btn_frame=Frame(self.master)
        btn_frame.pack(pady=10)

        tips1=Label(btn_frame,text="The default table is Student",fg='green')
        tips1.pack(side='left',padx=20)

        self.t_name='Student'
        self.s_num=None

        self.name=StringVar()
        self.c_select=ttk.Combobox(btn_frame,textvariable=self.name)
        try:
            lis=[]
            conn=sqlite3.connect("First.db")
            cur=conn.cursor()
            cur.execute("select name from sqlite_master where type='table'order by name")
            for row in cur.fetchall():
                lis.append(row[0])
        except:
            self.msg_box("fail to link database")
        finally:
            conn.close()
            self.c_select["values"]=(lis)
            self.c_select["state"]="readonly"
            #self.c_select.current(0)
            self.c_select.bind("<<ComboboxSelected>>",self.set_t_name)
            self.c_select.pack(side="left")
        
            

        btn1=Button(btn_frame,text="start")
        btn1.pack(side="left",padx=20)
        btn1.bind("<Button-1>",self.start)

        btn2=Button(btn_frame,text="end")
        btn2.pack(side="left",padx=20)
        btn2.bind("<Button-1>",self.end)

        btn3=Button(btn_frame,text="shift")
        btn3.pack(side="left",padx=20)
        btn3.bind("<Button-1>",self.shift)

        blur_frame=ttk.Frame(btn_frame)
        blur_frame.pack(side="left",padx=20)
        blur_label=Label(blur_frame,text="blur det:",fg='black')
        blur_label.pack(side='left')
        self.blur_E=Entry(blur_frame,width=10)
        self.blur_E.pack(side='left',padx=2)


        thre_frame1=ttk.Frame(btn_frame)
        thre_frame1.pack(side="left",padx=10)
        thre_label1=Label(thre_frame1,text="threshold :",fg='black')
        thre_label1.pack(side='left')
        self.thre_E1=Entry(thre_frame1,width=5)
        self.thre_E1.pack(side='left',padx=2)


        n=ttk.Notebook(self.master)
        f1=ttk.Frame(n,height=100,width=300)
        f2=ttk.Frame(n,height=100,width=300)
        n.add(f1,text="Absent")
        n.add(f2,text="Present")
        n.pack(side="bottom")

        self.lb_show1=Listbox(f1,bg="yellow",height=50,width=280)
        self.lb_show1.pack()
        self.lb_show1.bind("<Double-1>",self.modify_frame1)

        self.lb_show2=Listbox(f2,bg="yellow",height=50,width=280)
        self.lb_show2.pack()
        self.lb_show2.bind("<Double-1>",self.modify_frame2)
        try:
            conn=sqlite3.connect("First.db")
            cur=conn.cursor()
            cur.execute("update %s set pres=0"%self.t_name)
            cur.execute("select nums,name from %s"%self.t_name)
            for row in cur.fetchall():
                self.lb_show1.insert(END,row)
            conn.commit()
            
        except:
            self.msg_box("fail to link this database")
        finally:
            conn.close()
        
        self.count=0
            
        self.video_loop()

    def changestyle(self):
        self.style=-1*self.style

    def set_t_name(self,*arg):
        self.lb_show1.delete(0,END)
        self.lb_show2.delete(0,END)
        self.t_name=self.c_select.get()
        try:
            conn=sqlite3.connect("First.db")
            cur=conn.cursor()
            cur.execute("update %s set pres=0"%self.t_name)
            cur.execute("select nums,name from %s"%self.t_name)
            for row in cur.fetchall():
                self.lb_show1.insert(END,row)
            conn.commit()
            
        except:
            self.msg_box("fail to link this database")
        finally:
            conn.close()
    def shift(self,event):
        if self.camera.isOpened() and self.L_camera.isOpened() and self.shift_mark==1:
            self.camera = cv.VideoCapture(1)   
            self.L_camera=cv.VideoCapture(0)
            self.shift_mark*=-1
        elif self.camera.isOpened() and self.L_camera.isOpened():
            self.camera = cv.VideoCapture(0)   
            self.L_camera=cv.VideoCapture(1)
            self.shift_mark*=-1
        
    def modify_frame1(self,event):
        self.s_num=self.lb_show1.get(ACTIVE)
        m_frame=Toplevel(self.master)
        m_frame.wm_attributes("-topmost",1)
        m_frame.title("Modify")
                      
        self.m_name=StringVar()
        self.m_select=ttk.Combobox(m_frame,textvariable=self.m_name)
        self.m_select["values"]=("Present","Late")
        self.m_select["state"]="readonly"
        self.m_select.current(0)
        self.m_select.bind("<<ComboboxSelected>>",self.modify)
        self.m_select.pack()
    def modify_frame2(self,event):
        self.s_num=self.lb_show2.get(ACTIVE)
        m_frame=Toplevel(self.master)
        m_frame.wm_attributes("-topmost",1)
        m_frame.title("Modify")               
        self.m_name=StringVar()
        self.m_select=ttk.Combobox(m_frame,textvariable=self.m_name)
        self.m_select["values"]=("Absent","On-leave")
        self.m_select["state"]="readonly"
        self.m_select.current(0)
        self.m_select.bind("<<ComboboxSelected>>",self.modify)
        self.m_select.pack()
        
    def modify(self,event):
        try:
            conn=sqlite3.connect("First.db")
            cur=conn.cursor()
            lab_text=self.m_select.get()
            if lab_text=='Late':
                pass
            elif lab_text=="Present":                
                cur.execute("update %s set pres=1 where nums=%d"%(self.t_name,self.s_num[0]))
                cur.execute("update %s set times=times-1 where nums=%d"%(self.t_name,self.s_num[0]))
            elif lab_text=="Absent":
                cur.execute("update %s set pres=0 where nums=%d"%(self.t_name,self.s_num[0]))
                cur.execute("update %s set times=times+1 where nums=%d"%(self.t_name,self.s_num[0]))
            elif lab_text=="On-leave":
                pass
            self.lb_show1.delete(0,END)
            self.lb_show2.delete(0,END)    
            cur.execute('select nums,name from %s where pres=0'%self.t_name)
            for row in cur.fetchall():
                self.lb_show1.insert(END,row)

            cur.execute('select nums,name from %s where pres=1'%self.t_name)
            for row in cur.fetchall():
                self.lb_show2.insert(END,row)
            conn.commit()
        except:
            self.msg_box('Fail to modify')
        finally:
            conn.close()
    def video_loop(self):
        ret, img = self.camera.read()
        ret2=None
        if self.L_camera.isOpened():
            ret2,img2=self.L_camera.read()
        
        if ret:
            cv.waitKey(0)
            image_gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
            if self.style==1:
                faces=find_fac.find_faces(image_gray,1,self.face_cascade)
                for (x,y,w,h) in faces:
                    img = cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                if self.on_off == True and len(faces)>0 and self.count%self.interval==0:              
                    path='./test/raw_test_faces/'+str(self.count)+'p'+'.jpg'
                    cv.imwrite(path,image_gray)
                faces=[]
            elif self.style==-1:    
                if self.on_off == True and self.count%30==0:
                    path='./test/raw_test_faces/'+str(2*(self.count//30)-1)+'.jpg'
                    cv.imwrite(path,image_gray)
                    if ret2:
                        img2_gray=cv.cvtColor(img2,cv.COLOR_BGR2GRAY)
                        path2='./test/raw_test_faces/'+str(2*(self.count//30))+'.jpg'
                        cv.imwrite(path2,img2_gray)
                    self.p_count+=1
                    if self.p_count==5:
                        self.p_count=0
                        self.end(None)
                        
            cv2image = cv.cvtColor(img, cv.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)
            self.count+=1
            self.master.after(1, self.video_loop)


    def msg_box(self,T):
        self.msg=Toplevel(self.master)
        self.msg.wm_attributes("-topmost",1)
        self.msg.title("Message:")
        msg_T=Label(self.msg,text=T)
        msg_T.pack()

    def start(self,event):
        rm.del_file('./test/raw_test_faces')
        rm.del_file('./test/well_done_faces')
        self.lb_show1.delete(0,END)
        self.lb_show2.delete(0,END)
        
        if self.on_off==False:
            self.on_off=True
        else:
            pass
    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()
        if self.L_camera.isOpened():
            self.L_camera.release()
    def end(self,event):
        bl=self.blur_E.get()
        thre=self.thre_E1.get()

        if bl:
            self.blur_set=bl           
        if thre:
            self.threshold=thre            
        if self.on_off==True and len(os.listdir('./test/raw_test_faces'))>=1:
            self.on_off=False
            self.camera.release()
            self.L_camera.release()
            data_collect.to_test_database()
            
            table,filename_lis=face_matching.match(self.t_name,self.blur_set,self.threshold)
            d1={}
            d2={}
            if table!=False:
                try:
                    conn=sqlite3.connect("First.db")
                    cur=conn.cursor()

                    for i in range(len(table)):
                        d1.setdefault(table[i],table.count(table[i]))
                        d2.setdefault(table[i],filename_lis[i])

                    for gets1 in d1.keys():
                        if d1[gets1]>=3:
                            cur.execute("update %s set pres=%d where nums=%d"%(self.t_name,1,gets1))
                            
                    cur.execute('update %s set times=times+1 where pres=0'%self.t_name)
                    cur.execute('select nums,name from %s where pres=0'%self.t_name)
                    for row in cur.fetchall():
                        self.lb_show1.insert(END,row)

                    cur.execute('select nums,name from %s where pres=1'%self.t_name)
                    for row in cur.fetchall():
                        self.lb_show2.insert(END,row)
                     
                    conn.commit()
                except:
                    self.msg_box('database error')
                finally:
                        
                    conn.close()
            else:
                self.msg_box("can not find xml")

            for key1 in d2.keys():
                if d1[key1]>=3:
                    in_path='./test/well_done_faces/'+d2[key1]
                    img_temp=cv.imread(in_path)
                    cv.putText(img_temp,str(key1),(5,10),cv.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255),1)
                    filepath='./test_data/'+d2[key1]
                    cv.imwrite(filepath,img_temp)
            self.camera = cv.VideoCapture(0)  
            self.L_camera=cv.VideoCapture(1)

            try:
                conn=sqlite3.connect("First.db")
                cur=conn.cursor()
                cur.execute("update %s set pres=0"%self.t_name)
                conn.commit()
            except:
                self.msg_box("fail to link this database")
            finally:
                conn.close()

def check_Page():
    if not os.path.exists(r'./test'):
            os.mkdir(r'./test')
    if not os.path.exists(r'./test/raw_test_faces'):
            os.mkdir(r'./test/raw_test_faces')
    if not os.path.exists(r'./test/well_done_faces'):
            os.mkdir(r'./test/well_done_faces')
    global k_root
    k_root=Toplevel()
    k_root.geometry("1080x720")
    k_root.title("Attendance")
    K=K_APP(k_root)
    


