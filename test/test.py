import numpy as np
import os
from scipy.misc import imread, imresize
import os
from keras.models import load_model, Model
np.random.seed(30)
import random as rn
import joblib
import heapq
rn.seed(30)
#tf.random.set_seed(30)



def generator(source_path, folder_list, batch_size):
    print( 'Source path = ', source_path, '; batch size =', batch_size)
    img_idx = [0,1,2,4,6,8,10,12,14,16,18,20,22,24,26,27,28,29]
    #img_idx = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
    while True:
        #t = np.random.permutation(folder_list)
        t = folder_list
        num_batches = int(len(t)/batch_size)
        for batch in range(num_batches):
            batch_data = np.zeros((batch_size,18,128,128,3))
            batch_labels = np.zeros((batch_size,3))
            for folder in range(batch_size):
                imgs = os.listdir(source_path+'/'+ t[folder + (batch*batch_size)].split(';')[0])
                for idx,item in enumerate(img_idx):
                    #print(imgs[item])
                    #print(source_path+'/'+ t[folder + (batch*batch_size)].strip().split(';')[0]+'/'+imgs[item])
                    image = imread(source_path+'/'+ t[folder + (batch*batch_size)].strip().split(';')[0]+'/'+imgs[item]).astype(np.float32)
                    image = imresize(image,(128,128)).astype(np.float32)
                    '''
                    if image.shape[1] == 160:
                        image = imresize(image[:,20:140,:],(84,84)).astype(np.float32)
                    else:
                        image = imresize(image,(84,84)).astype(np.float32)
                    '''
                    batch_data[folder,idx,:,:,0] = image[:,:,0] - 104
                    batch_data[folder,idx,:,:,1] = image[:,:,1] - 117
                    batch_data[folder,idx,:,:,2] = image[:,:,2] - 123
                    
                batch_labels[folder, int(t[folder + (batch*batch_size)].strip().split(';')[2])] = 1
            yield batch_data, batch_labels

        if (len(t)%batch_size) != 0:
            batch_data = np.zeros((len(t)%batch_size,18,128,128,3))
            batch_labels = np.zeros((len(t)%batch_size,3))
            for folder in range(len(t)%batch_size):
                imgs = os.listdir(source_path+'/'+ t[folder + (num_batches*batch_size)].split(';')[0])
                for idx,item in enumerate(img_idx):
                    image = imread(source_path+'/'+ t[folder + (num_batches*batch_size)].strip().split(';')[0]+'/'+imgs[item]).astype(np.float32)
                    image = imresize(image,(128,128)).astype(np.float32)
                    '''
                    print(image.shape[1],image.shape[0])
                    if image.shape[1] == 460:
                        image = imresize(image[:,20:140,:],(84,84)).astype(np.float32)
                    else:
                        image = imresize(image,(84,84)).astype(np.float32)
                    '''

                    batch_data[folder,idx,:,:,0] = image[:,:,0] - 104
                    batch_data[folder,idx,:,:,1] = image[:,:,1] - 117
                    batch_data[folder,idx,:,:,2] = image[:,:,2] - 123

                batch_labels[folder, int(t[folder + (num_batches*batch_size)].strip().split(';')[2])] = 1

            yield batch_data, batch_labels
            

def inference():
    #Test Code
    
    #######
        
    model_name = 'C:/Users/Administrator/Desktop/Ankita/feature_extractor.h5'
    
    #######
        
    test_doc = open('C:/Users/Administrator/Desktop/Ankita/uploads/test.csv').readlines()
    test_path = 'C:/Users/Administrator/Desktop/Ankita/uploads'
    feature_matrix =joblib.load('C:/Users/Administrator/Desktop/Ankita/feature_matrix.pkl')
    num_test_sequences = len(test_doc)
    batch_size=1
    print ('# testing sequences =', num_test_sequences)
    print ('# batch size =', batch_size)
    test_generator = generator(test_path, test_doc, batch_size)
    model = load_model(model_name)
    print("Model loaded.")
    model_func = Model(inputs=[model.input], outputs=model.get_layer('flatten_14').output)
        
    num_batches = int(num_test_sequences/batch_size)
        
    test_feature_matrix = np.zeros([num_test_sequences, 32768])   # initialize the matrix with zeros
    #test_feature_matrix.shape
    #test_doc  
    
    for i in range(num_batches):
        x,true_labels = test_generator.__next__()
        print ("shape of x:", x.shape, "and shape of true_labels:", true_labels.shape)
        #pred_idx = np.argmax(model_func.predict_on_batch(x), axis=1)
        test_feature_matrix[i,:]=model_func.predict_on_batch(x)
    
    '''
    dot_product = feature_matrix.dot(feature_matrix.T)
    norms = np.array([np.sqrt(np.diagonal(dot_product))])
    similarity = dot_product / (norms * norms.T)
        
    len(feature_matrix[0,:])
    similarity.shape
    
    closest_ids = np.argsort(similarity[5, :])[::-1][0:2]
    '''
    a=feature_matrix
    b=test_feature_matrix   
    a_norm = np.linalg.norm(a, axis=1)
    b_norm = np.linalg.norm(b)
    result=np.dot(b,a.T) / (a_norm * b_norm)
    result.shape
    result=result.squeeze()
    closest_bowl_types=[]
    result=list(result)
    selected=heapq.nlargest(10,result)
    for r in selected:
        closest_bowl_types.append(result.index(r))
        
    return closest_bowl_types


