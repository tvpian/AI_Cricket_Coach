# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 19:47:58 2020

@author: IMGADMIN
"""

#Dataset generation tool

# Importing all necessary libraries
import cv2
import os

path1="C:/Users/Administrator/Desktop/BowlTypeDataset/Dataset/val/Offspin/"
os=os.listdir(path1)
length = len(os)
c_path1="C:/Users/Administrator/Desktop/BowlTypeDataset/Dataset/val/Offspin_val"

'''
for i in range(0,length):
    print(i)
    os.makedirs('Offspin_val'+str(i))
'''

import shutil
length = len(os)
for f in range(length):
    print(f)
    shutil.copy(path1+os[f], c_path1+str(f)+"/")
fv_s=[]
length = len(fv)
for f in range(length):
    fv_s.append("Fast_val"+str(f))

ls_s=[]
length = len(ls)
for f in range(length):
    ls_s.append("Legspin_val"+str(f))

osp_s=[]
length = len(os)
for f in range(length):
    osp_s.append("Offspin_val"+str(f))



f_v = os.listdir("C:/Users/Administrator/Desktop/BowlTypeDataset/Fast")
os

import os
import cv2

path="C:/Users/Administrator/Desktop/test_set/"
train_list=os.listdir(path)
train_len=len(train_list)
for index,name in enumerate(train_list):
    train_path="C:/Users/Administrator/Desktop/test_set/"+train_list[index]
    os.chdir(train_path)
    train_path_vid=train_path+"/"+os.listdir(train_path)[0]
    # Read the video from specified path
    cam = cv2.VideoCapture(train_path_vid)
    
    '''
    try:
        # creating a folder named data
        if not os.path.exists('data'):
            os.makedirs('data')
            # if not created then raise error
    except OSError:
        print('Error: Creating directory of data')
    '''

    # frame
    currentframe = 0
    i=0
    while(True):
        ret, frame = cam.read()
        if ret:
            if currentframe%2==0:
                '''
                name = './data/frame' + str(i) + '.jpg'
                print ('Creating...' + name) 
                # writing the extracted images 
                cv2.imwrite(name, frame) 
                '''
                
                img_name = str(name)+"_" + str(i) + '.jpg'
                print('Creating...' + img_name)
                frame=frame[100:560,433:893]
                cv2.imwrite(train_path+"/"+img_name, frame)
                
                # increasing counter so that it will
                # show how many frames are created
                i+=1
            currentframe+=1
        else:
            break
    # Release all space and windows once done 
    cam.release() 
    os.remove(train_path_vid)
    cv2.destroyAllWindows() 


import pandas as pd
fv_d=pd.DataFrame({0:fv_s,1:"Fast",2:0})
ls_d=pd.DataFrame({0:ls_s,1:"Legspin",2:1})
osp_d=pd.DataFrame({0:osp_s,1:"Offspin",2:2})


final=pd.concat([fv_d,ls_d,osp_d],ignore_index=True)


final.to_csv("val.csv",index=False,header=False,sep=";")


for i,y in enumerate(train_list):
    print(i,y)



import cv2
img = cv2.imread("frame1.jpg")
crop_img = img[100:560, 433:893]
cv2.imshow("cropped", crop_img)
cv2.waitKey(0)





#Test dataset creation
a=["Fast0","Fast1","Fast2","Legspin0","Legspin1","Legspin2","Offspin0","Offspin1"]
b=["Fast","Fast","Fast","Legspin","Legspin","Legspin","Offspin","Offspin"]
c=[0,0,0,1,1,1,2,2]
final=pd.DataFrame({0:a,1:b,2:c})

final.to_csv("train.csv",index=False,header=False,sep=";")

