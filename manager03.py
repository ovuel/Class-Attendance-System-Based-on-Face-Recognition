# -*- coding: cp936 -*-
#manage the student database
import os
from Tkinter import *
import ttk
import sqlite3
import training
class App:
    def __init__(self, master):
        self.master = master
        self.initWidgets()
    def initWidgets(self):
        topF = Frame(self.master)
        topF.pack()

        botF=Frame(self.master)
        botF.pack(side='bottom')

        tips_frame=Frame(topF)
        tips_frame.pack(side='left')

        self.t_name=None
        self.s_name=None
        self.s_num=None

        lab1=Label(tips_frame,text="Double click!")
        lab1.pack()
        lab2=Label(tips_frame,text="Be chosen:")
        lab2.pack()
        self.lab3=Label(tips_frame)
        self.lab3.pack()

        tips_frame2=Frame(botF)
        tips_frame2.pack(side='left')

        lab4=Label(tips_frame2,text="The student who is chosen:")
        lab4.pack()
        self.lab5=Label(tips_frame2)
        self.lab5.pack()
        
        # 创建Listbox组件
        self.lb = Listbox(topF)
        self.lb.pack(side=LEFT)

        self.lb2=Listbox(botF,selectmode=SINGLE)
        self.lb2.pack(side='left')


        #self.lb.bind("<Double-1>", self.click)
        self.lb2.bind("<Double-1>",self.click2)
        self.lb.bind("<Double-1>", self.look)
        


        scroll = Scrollbar(topF, command=self.lb.yview)
        scroll.pack(side='left',fill=Y)
        self.lb.configure(yscrollcommand=scroll.set)

        scroll2 = Scrollbar(botF, command=self.lb2.yview)
        scroll2.pack(side='left',fill=Y)
        self.lb2.configure(yscrollcommand=scroll2.set)
        

        BtnFrame=Frame(topF)
        BtnFrame.pack(side='left',padx=10)
        
        self.btn1=Button(BtnFrame,text="Add")
        self.btn1.pack(pady=5)
        self.btn1.bind("<Button-1>",self.add_table)

        self.btn2=Button(BtnFrame,text="Delete")
        self.btn2.pack()
        self.btn2.bind("<Button-1>",self.del_table)

        self.e_show=Entry(topF,width=10)
        self.e_show.pack(side='right',padx=10)

        lab4=Label(topF,text="(Class Id:)")
        lab4.pack(side='right',padx=10)
        
        BtnFrame2=Frame(botF)
        BtnFrame2.pack(side='left',padx=10)
        
        self.btn3=Button(BtnFrame2,text="Add student")
        self.btn3.pack(pady=5)
        self.btn3.bind("<Button-1>",self.add_student)

        self.btn4=Button(BtnFrame2,text="Delete student")
        self.btn4.pack()
        self.btn4.bind("<Button-1>",self.del_student)

        self.btn5=Button(BtnFrame2,text="Delete all")
        self.btn5.pack(pady=5)
        self.btn5.bind("<Button-1>",self.del_all)

        self.btn6=Button(BtnFrame2,text="Train")
        self.btn6.pack(pady=5)
        self.btn6.bind("<Button-1>",self.train_data)

        try:
            conn=sqlite3.connect("First.db")
            cur=conn.cursor()
            cur.execute('''Create Table If Not Exists Student(nums int,name text,pres boolean,times int,path text)''')
            cur.execute("select name from sqlite_master where type='table'order by name")
            for row in cur.fetchall(): 
                self.lb.insert(END, row)
        except:
            self.msg_box("Fail to link the database.")
        finally:
            conn.close()
    def train_data(self,event):
        diction={}
        if self.t_name:
            try:
                conn=sqlite3.connect("First.db")
                cur=conn.cursor()
                cur.execute("select nums,path from %s"%self.t_name)
                for row in cur.fetchall():
                    f_path='./train/train_database/'+str(row[0])
                    if os.path.exists(f_path):
                        diction.setdefault(row[0],row[1])
                    else:
                        self.msg_box("File %d can not be found"%row[0])
                        continue
                training.face_training(diction,self.t_name)
                self.msg_box("Train Done!")
            except:
                self.msg_box("Fail to train data")
            finally:
                conn.close()
            
        
    def del_all(self,event):
        try:
            conn=sqlite3.connect("First.db")
            cur=conn.cursor()
            cur.execute("delete from %s"%self.t_name[0])
            self.lb2.delete(0,END)
        except:
            self.msg_box("del_all error!")
        finally:
            conn.commit()
            conn.close()

    def add_student(self,event):
        add_frame=Toplevel(root)
        add_frame.geometry("320x420")
        add_frame.wm_attributes("-topmost",1)
        add_frame.title("Select students from table")

        show_frame=Frame(add_frame)
        show_frame.pack()
        
        self.lb_show=Listbox(show_frame,width=30,height=20,selectmode=EXTENDED)
        self.lb_show.pack(side='left')
        self.lb_show.bind("<Double-1>",self.click)

        scroll3 = Scrollbar(show_frame, command=self.lb_show.yview)
        scroll3.pack(side='left',fill=Y)
        self.lb_show.configure(yscrollcommand=scroll3.set)

        tip1=Label(add_frame,text="Double click and insert it into class table")
        tip1.pack(pady=5)
        try:
            conn=sqlite3.connect("First.db")
            cur=conn.cursor()
            cur.execute("select nums,name from Student where not exists(select 1 from %s where %s.nums=Student.nums)"%(self.t_name[0],self.t_name[0]))
            for row in cur.fetchall():
                self.lb_show.insert(END,row)
        except:
            self.msg_box("link database error!")
        finally:
            conn.close()

    def del_student(self,event):
        #print self.t_name[0]
        #print self.s_name[0]
        if self.s_name and self.t_name:
            try:
                conn=sqlite3.connect("First.db")
                cur=conn.cursor()
                cur.execute('delete from %s where nums=%d'%(self.t_name[0],self.s_name[0]))
                self.lb2.delete(0,END)
                cur.execute('select nums,name,times from %s'%self.t_name)
                for row in cur.fetchall():
                    self.lb2.insert(END,row)
            except:
                self.msg_box("can not delete this data!")
            finally:
                conn.commit()
                conn.close()
        
    def click(self, event):
        self.s_num=self.lb_show.get(self.lb_show.curselection())
        self.lb_show.delete(self.lb_show.curselection())
        #print self.s_num, self.t_name
        try:
            conn=sqlite3.connect("First.db")
            cur=conn.cursor()
            cur.execute("insert into %s select * from Student where Student.nums=%d"%(self.t_name[0],self.s_num[0]))
            self.lb2.insert(END,self.s_num)
        except:
            self.msg_box("fail to insert!")
        finally:
            conn.commit()
            conn.close()
    
    def click2(self, event):
        # 获取Listbox当前选中项
        self.s_name=self.lb2.get(ACTIVE)
        self.lab5["text"]=self.s_name[0:2]
        #print self.s_name


    def add_table(self,event):
        tb_name=self.e_show.get()
        if tb_name:
            try:
                conn=sqlite3.connect("First.db")
                cur=conn.cursor()
                cur.execute('''create table '%s'(nums int,name text,pres boolean,times int,path text)'''%tb_name)
                self.lb.delete(0,END)
                cur.execute("select name from sqlite_master where type='table'order by name")
                for row in cur.fetchall(): 
                    self.lb.insert(END, row)
                conn.commit()
            except:
                self.msg_box("fail to add a table")
            finally:
                conn.close()
            self.e_show.delete(0,END)
    def del_table(self,event):
        if self.t_name:
            try:
                conn=sqlite3.connect("First.db")
                cur=conn.cursor()
                cur.execute("drop table '%s'"%self.t_name)
                self.lb.delete(0,END)
                cur.execute("select name from sqlite_master where type='table'order by name")
                for row in cur.fetchall(): 
                    self.lb.insert(END, row)
                conn.commit()
            except:
                self.msg_box("fail to delete the table")
            finally:
                conn.close()
                
        else:
            self.msg_box("Please choose a table name firstly.")
        self.lb2.delete(0,END)
        self.t_name=None
    def look(self,event):      
        self.lb2.delete(0,END)
        self.t_name=self.lb.get(ACTIVE)
        self.lab3["text"]=self.t_name
        try:
            conn=sqlite3.connect("First.db")
            cur=conn.cursor()
            cur.execute('select nums,name,times from %s'%self.t_name)
            for row in cur.fetchall():
                self.lb2.insert(END,row)
        except:
            print("fail to search table")
        finally:
            conn.close()
    def msg_box(self,T):
        self.msg=Toplevel(root)
        self.msg.wm_attributes("-topmost",1)
        self.msg.title("Message:")
        msg_T=Label(self.msg,text=T)
        msg_T.pack()

def db_Page():
    if not os.path.exists('./train/index'):
            os.mkdir('./train/index')
    global root
    root = Toplevel()
    root.geometry("640x480")
    root.title("Database manager")
    App(root)


