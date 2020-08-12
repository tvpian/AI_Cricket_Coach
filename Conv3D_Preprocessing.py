# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 19:47:58 2020

@author: IMGADMIN
"""

#Dataset generation tool

# Importing all necessary libraries
import cv2
import os
import pandas as pd


def preprocess(path):
    filepath=path
    path = os.path.dirname(filepath)
    files=os.listdir(path)
    length = len(files)
    
    frame_path=path+"/"+'Test0/'
    test_list=os.listdir(path)
    #test_len=len(test_list)
    for i in range(0,length):
        print(i)
        os.makedirs(path+"/"+'Test'+str(i))
    for index,name in enumerate(test_list):
        os.chdir(frame_path)
        test_path_vid=filepath
        # Read the video from specified path
        cam = cv2.VideoCapture(test_path_vid)
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
                    cv2.imwrite(img_name, frame)
                    
                    # increasing counter so that it will
                    # show how many frames are created
                    i+=1
                currentframe+=1
            else:
                break
        # Release all space and windows once done 
        cam.release() 
        #os.remove(train_path_vid)
        cv2.destroyAllWindows() 
    
    test_d=pd.DataFrame({0:["Test0"],1:"test",2:0})
    os.chdir(path)
    test_d.to_csv("test.csv",index=False,header=False,sep=";")


#preprocess("C:/Users/Administrator/Desktop/Ankita/uploads/Test.webm")

