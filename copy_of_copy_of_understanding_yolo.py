# -*- coding: utf-8 -*-
"""Copy of Copy of Understanding yolo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13Oj22I3n9ZJ43RyXiiNr93UKBGQjFhOz
"""

!apt-get install -y -qq software-properties-common python-software-properties module-init-tools
!add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null
!apt-get update -qq 2>&1 > /dev/null
!apt-get -y install -qq google-drive-ocamlfuse fuse
from google.colab import auth
auth.authenticate_user()
from oauth2client.client import GoogleCredentials
creds = GoogleCredentials.get_application_default()
import getpass
!google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL
vcode = getpass.getpass()
!echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}

!mkdir -p drive
!google-drive-ocamlfuse drive

cd drive/project_data

cd Yolo_type_data/

import keras
from keras.models import Sequential
from keras import layers
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense, Reshape
from keras.layers.normalization import BatchNormalization
from keras import optimizers
import numpy as np
import tensorflow as tf
from keras.optimizers import SGD

X = np.load('X.npy')
Y = np.load('49*6lable.npy')

def add_vgg(model, shape=(300,300,3)):
    
    # Block 1
    model.add(Conv2D(64, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block1_conv1',input_shape=shape,
                      trainable=False))
    model.add(Conv2D(64, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block1_conv2',
                      trainable=False))
    model.add(MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool'))
    model.add(BatchNormalization())

    # Block 2
    model.add(Conv2D(128, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block2_conv1',
                      trainable=False))
    model.add(Conv2D(128, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block2_conv2',
                      trainable=False))
    model.add(MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool'))
    model.add(BatchNormalization())

    # Block 3
    model.add(Conv2D(256, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block3_conv1',
                      trainable=False))
    model.add(Conv2D(256, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block3_conv2',
                      trainable=False))
    model.add(Conv2D(256, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block3_conv3',
                      trainable=False))
    model.add(MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool'))
    model.add(BatchNormalization())

    # Block 4
    model.add(Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block4_conv1',
                      trainable=False))
    model.add(Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block4_conv2',
                      trainable=False))
    model.add(Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block4_conv3',
                      trainable=False))
    model.add(MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool'))
    model.add(BatchNormalization())

    # Block 5
    model.add(Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block5_conv1',
                      trainable=False))
    model.add(Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block5_conv2',
                      trainable=False))
    model.add(Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='block5_conv3',
                      trainable=False))
    model.add(MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool'))
    model.add(BatchNormalization())

    return model

#VGG structure model

def add_extra_layers(model):
    #extra Block
    model.add(Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='extra_block_conv1'))
    model.add(Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='extra_block_conv2'))
    model.add(Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='extra_block_conv3'))
    
    #Padding removed(To bring the proper shape)
    
    model.add(Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='extra_block_conv4'))
    model.add(Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='extra_block_conv5'))
    model.add(Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      name='extra_block_conv6'))
    return model

def add_final_layer(model):
    
    #final extra Block
    model.add(Conv2D(256, (3, 3),
                      activation='relu',
                      name='final_block1_conv1'))
    model.add(Conv2D(128, (3, 3),
                      activation='relu',
                      padding='same',
                      name='final_block_conv2'))
    model.add(Flatten())
    model.add(Dense(600))
    model.add(Dense(294))
    model.add(Reshape((49, 6)))
    return model

def create_model(inp_shape=(300,300,3)):
    #Declaring Sequential model
    model = Sequential()
    # Loading VGG model structure
    model = add_vgg(model)
    model.load_weights('classifier_weights.h5',by_name=True)
    model = add_extra_layers(model)
    model = add_final_layer(model)
    # Loading trained VGG weights to the named layers
    
    
    
    return model

from keras import backend as K

def C_Loss(Y_true, Y_pred):
    c_true = Y_true[:,:,5:6]
    c_pred = Y_pred[:,:,5:6]
    pred_  = Y_pred[:,:,0:5]
    true_  = Y_true[:,:,0:5]
    loss1 = tf.square(tf.subtract(c_true,c_pred))
    loss2 = tf.multiply(c_true,tf.square(tf.subtract(pred_,true_)))
    return (loss1+loss2)

#model = create_model()
sgd = SGD(lr=0.0001)
model.compile(loss=C_Loss,
              optimizer=sgd,
              metrics=['accuracy'])

print(X.shape)
print(Y.shape)

model.save_weights('detector.h5')

model.fit(X[0:16000], Y[0:16000], batch_size=64, epochs=10, verbose=1,validation_data=(X[16000:],Y[16000:]))

model.predict(X[0:1])

