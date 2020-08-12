# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 22:13:39 2020

@author: IMGADMIN
"""
from scipy import spatial
from sklearn.preprocessing import normalize
import numpy as np
from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()

def shot_similarity(player_shot,refernece_shot): 
    #d1=[[-0.5, 1.2, -9.1,0,-1,0],[-0.55, 1.2, -8.5,0,-1,0],[-0.58, 1.2, -8.3,0,-1,0],[-0.6, 1.2, -8.0,0,-1,0],[-0.65, 1.2, -7.8,-15,-1,0],[-0.68, 1.2, -7.7,-19,-1,0],[-0.7, 1.2, -7.5,-20,-1,0],[-0.72, 1.2, -7.3,-25,-1,0]]
    #d2=[[-0.5, 1.2, -9.1,0,0,0],[-0.5, 1.2, -8.5,0,0,0],[-0.5, 1.2, -8.3,0,0,0],[-0.5, 1.2, -8.0,0,0,0],[-0.5, 1.2, -7.8,0,0,0],[-0.5, 1.2, -7.7,-20,0,0],[-0.5, 1.2, -7.5,-29,0,0],[-0.5, 1.2, -7.3,-30,0,0]]
    d1=player_shot
    d2=refernece_shot
    """
    d1#2d dataset input
    d2#2d dataset input
    """
    #for cosine similarity validation
    d3=[[-0.8, 1.2, -19.1,0,0,30],[-0.5, 1.2, -8.5,0,24,0],[-0.5, 1.2, -8.3,0,0,0],[-0.5, 1.2, -8.0,0,0,0],[-0.5, 1.2, -7.8,0,0,0],[-0.5, 1.2, -7.7,-20,0,0],[-0.5, 1.2, -7.5,-29,0,0],[-0.5, 1.2, -7.3,-30,0,0]]
    np1=[] #normalization position
    na1=[]#normalization angle
    for i in range(8):
        for j in range(6):
            if(j<3):
                np1.append(d1[i][j])
               
            else:
                na1.append(d1[i][j])            
    np2=[]#normalization position
    na2=[]#normalization angle
    for i in range(8):
        for j in range(6):
            if(j<3):
                np2.append(d2[i][j])
               
            else:
                na2.append(d2[i][j])
    # converting into 2d array for performing min max normalization
    np1=np.array(np1).reshape(-1,1)
    np2=np.array(np2).reshape(-1,1)
    na1=np.array(na1).reshape(-1,1)
    na2=np.array(na2).reshape(-1,1) 
    np1=min_max_scaler.fit_transform(np1)
    np2=min_max_scaler.fit_transform(np2)
    na1=min_max_scaler.fit_transform(na1)
    na2=min_max_scaler.fit_transform(na2)
    # converting again into 1d array and list
    np1=list(np1.flatten())
    np2=list(np2.flatten())
    na1=list(na1.flatten())
    na2=list(na2.flatten())
    d1n = np.zeros(shape=(8,6))#normalized 2d dataset
    d2n = np.zeros(shape=(8,6))#normalized 2d dataset
    for i in range(8):
        k=-1
        for j in range(6):
            if(j<3):
                d1n[i][j]=np1[i*3+j]
               
            else:
                k=k+1
                d1n[i][j]=na1[i*3+k]
    for i in range(8):
        k=-1
        for j in range(6):
            if(j<3):
                d2n[i][j]=np2[i*3+j]
               
            else:
                k=k+1
                d2n[i][j]=na2[i*3+k]  
    result=0
    for i in range(8):
        result =result+ 1 - spatial.distance.cosine(d1n[i], d2n[i])
       
    return result/8

