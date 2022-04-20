# -*- coding: cp936 -*-
import cv2 as cv
import numpy as np
import math
from matplotlib import pyplot as plt

def img_trans(images,eye_cascade):
    
    ###会出现误检测！！！
    ###在脸的上半部分对眼睛检测
    rows,cols=images.shape
    mid_h=rows//2
    Top_img=images[0:mid_h,0:cols]
    eyes = eye_cascade.detectMultiScale(Top_img,1.05,5,0,(5,5))
    
    if len(eyes)!=2 or eyes[0,0]-eyes[1,0]==0:
        eyes=eye_cascade.detectMultiScale(Top_img,1.05,5,0,(15,15))
    if len(eyes)!=2 or eyes[0,0]-eyes[1,0]==0:
        eyes=eye_cascade.detectMultiScale(Top_img,1.05,5,0,(25,25))
    if len(eyes)!=2 or eyes[0,0]-eyes[1,0]==0:
        eyes=eye_cascade.detectMultiScale(Top_img,1.05,5,0,(35,35))
    '''
    if cols>=150:
        eyes=eye_cascade.detectMultiScale(Top_img,1.05,5,0,(30,30))
    elif cols>=100:
        eyes=eye_cascade.detectMultiScale(Top_img,1.05,5,0,(20,20))
    elif cols>=60:
        eyes=eye_cascade.detectMultiScale(Top_img,1.05,5,0,(10,10))
    '''
    if len(eyes)!=2 or eyes[0,0]-eyes[1,0]==0:
        print "fail to find eyes"
        return images[5:cols-5,5:rows-5]
    else:
        L_iris=[eyes[0,0]+eyes[0,2]//2,eyes[0,1]+eyes[0,3]//2]
        R_iris=[eyes[1,0]+eyes[1,2]//2,eyes[1,1]+eyes[1,3]//2]
        eyes_center = [(L_iris[0]+R_iris[0])//2,(L_iris[1]+R_iris[1])//2]
        temp=math.atan(float(eyes[0,1]-eyes[1,1])/float(eyes[0,0]-eyes[1,0]))
        r=math.degrees(temp)
        eyes_dis=float((eyes[0,0]-eyes[1,0])**2+(eyes[0,1]-eyes[1,1])**2)**0.5
        
        p=0.4      #修改人脸大小占图片的比例
        scale=cols*p/eyes_dis

        mark_h=rows//3

        bias_x=cols//2-eyes_center[0]
        bias_y=mark_h-eyes_center[1]
        #平移
        N = np.float32([[1,0,bias_x],[0,1,bias_y]])
        M=cv.getRotationMatrix2D((eyes_center[0],eyes_center[1]),r,scale)

        images=cv.warpAffine(images,M,(cols,rows))
        dst=cv.warpAffine(images,N,(cols,rows))
      
        return dst


def img_masking(images):
    img=images
    rows,cols=img.shape
    ellipse=np.zeros(img.shape[0:2],dtype="uint8")
    cv.ellipse(ellipse,(cols//2,rows//2),(int(cols*0.5*0.8),int(rows*0.5*0.95)),0,0,360,255,-1)
    mask=ellipse
    masked=cv.bitwise_and(img,img,mask=mask)
    return masked

def border(images):
    roi_g=images
    h,w=roi_g.shape
    top,bottom,left,right=(0,0,0,0)
    longest_edge = max(h, w)
    # 计算短边需要增加多上像素宽度使其与长边等长
    if h < longest_edge:
        dh = longest_edge - h
        top = dh // 2
        bottom = dh - top
    elif w < longest_edge:
        dw = longest_edge - w
        left = dw // 2
        right = dw - left
    else:
        pass

    BLACK=[0]

    # 给图像增加边界，是图片长、宽等长，cv2.BORDER_CONSTANT指定边界颜色由value指定
    roi = cv.copyMakeBorder(roi_g, top, bottom, left, right, cv.BORDER_CONSTANT, value=BLACK)
    return roi


def equ(image):
    image=image[:,0:image.shape[1]-2]
    h,w=image.shape
    mid_w=w//2
    img_L=image[0:h,0:mid_w]
    img_R=image[0:h,mid_w:w]

    wl=img_L.shape[1]
    wr=img_R.shape[1]
    
    image=cv.equalizeHist(image)
    img_L=cv.equalizeHist(img_L)
    img_R=cv.equalizeHist(img_R)
    
    image[0:h,0:w//4]=img_L[0:h,0:wl//2]
    image[0:h,mid_w+wr//2:w]=img_R[0:h,wr//2:wr]

    cols_num1=mid_w-w//4
    cols_num2=wr//2

    for i in range(w//4,mid_w+wr//2):
        if i< mid_w:
            weight=float(1)/cols_num1*(i-w//4)
            image[:,i]=image[:,i]*weight+img_L[:,i]*(1-weight)
        else:
            weight=float(1)/cols_num2*(i-mid_w)
            image[:,i]=image[:,i]*(1-weight)+img_R[:,i-mid_w]*weight

    return image


def preprocess(image,flag=None,eye_cascade=None):
    img=image
    if flag==1:
        img=img_trans(img,eye_cascade)
    img=equ(img)

    img = cv.bilateralFilter(img,2,8,6)#双边滤波器平滑处理
    
    img=border(img)

    img = img_masking(img)
    
    return img

    




