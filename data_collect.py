# -*- coding: cp936 -*-
#用于生成测试数据库和训练数据库
import pre
import os
import cv2 as cv
import numpy as np
import find_fac as ffc
        
#生成一个测试集
def to_test_database():
    eye_cascade = cv.CascadeClassifier(r'./data/haarcascade_eye.xml')
    face_cascade = cv.CascadeClassifier(r'./data/haarcascade_frontalface_alt.xml')
    input_path=r'./test/raw_test_faces/'
    tdb_path=r'./test/well_done_faces/'
    for filename in os.listdir(input_path):
        filepath=input_path+filename
        img_input=cv.imread(filepath,0)
        img_p=ffc.find_faces(img_input,2,face_cascade)
        if img_p:
            t=filename.index('.')
            for i in range(len(img_p)):
                output=tdb_path+filename[0:t]+'_'+str(i)+'.jpg'
                img_dst=pre.preprocess(img_p[i],1,eye_cascade)
                cv.imwrite(output,img_dst)
        

   
    
