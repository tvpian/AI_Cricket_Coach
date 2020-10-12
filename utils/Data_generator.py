# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 16:02:22 2020

@author: IMGADMIN
"""


import pandas as pd
import numpy as np
import os
from scipy.misc import imread, imresize
import datetime
import os
from keras.models import Sequential
from keras.layers import Dense, GRU, Dropout, Flatten, BatchNormalization, Activation
from keras.layers.convolutional import Conv3D, MaxPooling3D
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout


# Importing the dataset
train = pd.read_csv('train.csv',header=None)
test = pd.read_csv('val.csv',header=None)
train_set=train.iloc[:,:].values
test_set=train.iloc[:,:].values
X_train = train.iloc[:,:-1].values
y_train = train.iloc[:,-1].values
X_test = test.iloc[:,:-1].values
y_test = test.iloc[:,-1].values






'''
# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc.fit(X_train)
X_train=sc.transform(X_train)
X_test = sc.transform(X_test)
'''



# Feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
sc.fit(X_train)

'''
model = Sequential() 
#batch_size = 32 
model.add(LSTM(128, activation='relu', input_shape=(20, 2), return_sequences=True)) 
# model.add(Dropout(0.2)) 
 
model.add(LSTM(128, activation='relu')) 
# model.add(Dropout(0.2)) 
 
model.add(Dense(32, activation='relu')) 
# model.add(Dropout(0.2)) 
 
model.add(Dense(1, activation='sigmoid')) 
 
opt = optimizers.Adam(lr = 1e-3, decay = 1e-5) 
 
model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy']) 


model.fit_generator(train_generator, steps_per_epoch=steps_per_epoch, epochs=num_epochs, verbose=1, 
                    callbacks=callbacks_list, validation_data=val_generator, 
                    validation_steps=validation_steps, class_weight=None, workers=1, initial_epoch=0)

'''


# Part 2 - Building the RNN

# Initialising the RNN
model = Sequential()

# Adding the first LSTM layer and some Dropout regularisation
model.add(LSTM(units = 50, return_sequences = True, input_shape=(20, 2)))
model.add(Dropout(0.2))

# Adding a second LSTM layer and some Dropout regularisation
model.add(LSTM(units = 50, return_sequences = True))
model.add(Dropout(0.2))

# Adding a third LSTM layer and some Dropout regularisation
model.add(LSTM(units = 50, return_sequences = True))
model.add(Dropout(0.2))

# Adding a fourth LSTM layer and some Dropout regularisation
model.add(LSTM(units = 50))
model.add(Dropout(0.2))

# Adding the output layer
model.add(Dense(1, activation='sigmoid')) 
 
#opt = optimizers.Adam(lr = 1e-3, decay = 1e-5) 
 
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) 

'''
model.fit_generator(train_generator, steps_per_epoch=steps_per_epoch, epochs=num_epochs, verbose=1, 
                    callbacks=callbacks_list, validation_data=val_generator, 
                    validation_steps=validation_steps, class_weight=None, workers=1, initial_epoch=0)
'''

 
#model.fit(x_train, y_train, epochs=3, batch_size=20, validation_data = (x_test, y_test)) 

def generator(dataframe, batch_size,normalizer):
    #print( 'Source path = ', source_path, '; batch size =', batch_size)
    #img_idx = [0,1,2,4,6,8,10,12,14,16,18,20,22,24,26,27,28,29]
    #img_idx = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
    while True:
        t = dataframe
        num_batches = int(len(t)/batch_size)
        for batch in range(num_batches):
            batch_data = np.zeros((batch_size,20,2))
            batch_labels = np.zeros((batch_size,1))
            for index in range(batch_size):
                i=batch*batch_size+index
                a=t.iloc[i,:-1]
                a=normalizer.transform(np.array(a).reshape(1,-1))
                a=np.squeeze(a)
                labels=t.iloc[i,-1]
                labels=np.array(labels)
                nl=[]
                for j in range(len(a)):
                    if j%2==0:
                        nl.append([a[j],a[j+1]])
                    j=j+1
                nl_a=np.array(nl)
                batch_data[index]=nl_a
                batch_labels[index]=labels
            yield batch_data,batch_labels
            
        if (len(t)%batch_size) != 0:
            batch_data = np.zeros((len(t)%batch_size,30,256,256,3))
            batch_labels = np.zeros((len(t)%batch_size,3))
            for batch in range(num_batches):
                batch_data = np.zeros((batch_size,20,2))
                batch_labels = np.zeros((batch_size,1))
                for index in range(batch_size):
                    i=batch*batch_size+index
                    a=t.iloc[i,:-1]
                    a=normalizer.transform(np.array(a).reshape(1,-1))
                    a=np.squeeze(a)
                    labels=t.iloc[i,-1]
                    labels=np.array(labels)
                    nl=[]
                    for j in range(len(a)):
                        if j%2==0:
                            nl.append([a[j],a[j+1]])
                        j=j+1
                    nl_a=np.array(nl)
                    batch_data[index]=nl_a
                    batch_labels[index]=labels
            yield batch_data,batch_labels
            
curr_dt_time = datetime.datetime.now()
num_train_sequences = len(train)
batch_size = 10
print('# training sequences =', num_train_sequences)
num_val_sequences = len(test)
print('# validation sequences =', num_val_sequences)
num_epochs = 100
print ('# epochs =', num_epochs)
            

#sgd = optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.7, nesterov=True)
#model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['categorical_accuracy'])
print (model.summary())
         
train_generator = generator(train,batch_size,sc)
val_generator = generator(test,batch_size,sc)
model_name = 'model_init' + '_' + str(curr_dt_time).replace(' ','').replace(':','_') + '/'
    
if not os.path.exists(model_name):
    os.mkdir(model_name)
        
filepath = model_name + 'model-{epoch:05d}-{loss:.5f}-{val_loss:.5f}.h5'

checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=False, save_weights_only=False, mode='auto', period=1)

#LR = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, verbose=1, mode='min', epsilon=0.0001, cooldown=0, min_lr=0.00001)
callbacks_list = [checkpoint]#, LR]


if (num_train_sequences%batch_size) == 0:
    steps_per_epoch = int(num_train_sequences/batch_size)
else:
    steps_per_epoch = (num_train_sequences//batch_size) + 1

if (num_val_sequences%batch_size) == 0:
    validation_steps = int(num_val_sequences/batch_size)
else:
    validation_steps = (num_val_sequences//batch_size) + 1
    
    
model.fit_generator(train_generator, steps_per_epoch=steps_per_epoch, epochs=num_epochs, verbose=1, validation_data=val_generator, callbacks=callbacks_list, 
                    validation_steps=validation_steps, class_weight=None, workers=1, initial_epoch=30)





### Test Code
trial=X_test[45]
label=y_test[45]
trial = np.array(trial)
test=sc.transform(trial.reshape(1,-1))#.reshape(1,-1))
test = np.reshape(test, (1,20, 2))


predicted_class = model.predict(test)
predicted_label = (predicted_class >0.5,"Right","Left")