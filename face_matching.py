# -*- coding: cp936 -*-
#������������ģ��ƥ�䲢���ؽ����
import cv2 as cv
import numpy as np
import os
def match(name,blur_set,thre):
    print blur_set,thre
    model=cv.face.LBPHFaceRecognizer_create()
    try:
        model.read("./train/index/%s.xml"%name)
    except:
        return False
    
    input_path=r'./test/well_done_faces'
    table=[]
    filename_lis=[]
    for filename in os.listdir(input_path):
        filepath=input_path+'/'+filename
        rois=cv.imread(filepath,0)
        blur=cv.Laplacian(rois, cv.CV_64F).var()
        if blur>int(blur_set):
            params=model.predict(rois)
            if params[1]<=int(thre):
                table.append(params[0])
                filename_lis.append(filename)
        else:
            continue
        print(filename,params,blur)
    print table

    return table,filename_lis

