# -*- coding: cp936 -*-
#检测人脸
#flag=1:实时检测；flag=2：非实时检测；flag=3：数据录入时检测
import cv2 as cv
import numpy
def find_faces(image,flag,face_cascade=None):
    

    if flag==1:
        faces = face_cascade.detectMultiScale(image, 1.25, 3,1,(50,50))      
    elif flag==2:
        clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img = clahe.apply(image)
        faces = face_cascade.detectMultiScale(img, 1.05, 5,1,(40,40))
    else:    
        faces = face_cascade.detectMultiScale(image, 1.05, 3,4)


    if flag==1:
        return faces
    
    elif flag==2:
        if len(faces)==0:
            face_set=[]
        else:
            face_set=[]
            for (x,y,w,h) in faces:
                face_set.append(image[y:y+h, x:x+w])
        return face_set
    else:  
        if len(faces)==1:
            roi_gray = image[faces[0][1]:faces[0][1]+faces[0][3], faces[0][0]:faces[0][0]+faces[0][2]]
        else:
            roi_gray=image
            print('find no face')
        return roi_gray
