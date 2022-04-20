# -*- coding: cp936 -*-
#ѵ��ʶ��ģ�Ͳ�����Ϊxml
import os
import cv2 as cv
import numpy as np
import sys


def read_images(dic):
    X,y=[],[]
    
    for get_key in dic:
        filepath=dic[get_key]        
        for filename in os.listdir(filepath):
            try:
                if(filename==".directory"):
                    continue
                imgpath=os.path.join(filepath,filename)
                im=cv.imread(imgpath,0)

                X.append(np.asarray(im,dtype=np.uint8))
                y.append(get_key)

            except IOError, (errno,strerror):
                print "I/O error({0}):{1}".format(errno,strerror)
            except:
                print "Unexpected error:",sys.exc_info()[0]
                raise
            
    return [X,y]


def face_training(dic,table_name):
    
    [X,y]=read_images(dic)
    y=np.asarray(y,dtype=np.int32)

    #model=cv.face.EigenFaceRecognizer_create() #���ɷ���Ŀ�����Ŷ���ֵ
    #model=cv.face.FisherFaceRecognizer_create()
    model=cv.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(X),np.asarray(y))
    model.save('./train/index/%s.xml'%table_name)
    



















    
