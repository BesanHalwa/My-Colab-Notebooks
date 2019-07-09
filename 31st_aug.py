# -*- coding: utf-8 -*-
"""31st Aug.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AsAnJH3vy5KOE-I5TlZbN_Wdi7jKMvOw
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

cd drive/project_data/

import keras
from keras import backend as K
import tensorflow as tf
import tensorflow
from keras.models import Model
from keras import layers
from keras.models import Sequential
from keras.layers import Reshape, Activation, Conv2D, Input, MaxPooling2D, BatchNormalization, Flatten, Dense, Lambda
from keras.layers.advanced_activations import LeakyReLU, Softmax
from keras.layers.merge import concatenate
from keras.optimizers import SGD, Adam, RMSprop
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard

import numpy as np
import os
import cv2
import math

X = np.load('final_pascal_npy_datas/2007_test.npy')
Y = np.load('fixed_labels/2007_test_labels.npy')

print(X.shape)
Y.shape



def CrossEntropy(y_pred, y_true):
    if y == 1:
      return -log(yHat)
    else:
      return -log(1 - yHat)

def ultimate_loss(y_true, y_pred):

  loss = tf.reduce_sum(tf.nn.sigmoid_cross_entropy_with_logits(labels=y_true, logits=y_pred)) / 42

  return loss

input_image = Input(shape=(300, 300, 3)) 
#input_image = tf.convert_to_tensor(np.zeros(shape=(300,300,3)))

#############################################################
####### VGG16 Model  ########################################
#############################################################
# Block 1
net = layers.Conv2D(64, (3, 3),
                  activation='relu',
                  padding='same',
                  name='block1_conv1', trainable=False)(input_image)
net = BatchNormalization()(net)
net = layers.Conv2D(64, (3, 3),
                  activation='relu',
                  padding='same',
                  name='block1_conv2', trainable=False)(net)
net = BatchNormalization()(net)
net = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(net)

# Block 2
net = layers.Conv2D(128, (3, 3),
                  activation='relu',
                  padding='same',
                  name='block2_conv1', trainable=False)(net)
net = BatchNormalization()(net)
net = layers.Conv2D(128, (3, 3),
                  activation='relu',
                  padding='same',
                  name='block2_conv2', trainable=False)(net)
net = BatchNormalization()(net)
net = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(net)

# Block 3
net = layers.Conv2D(256, (3, 3),
                  activation='relu',
                  padding='same',
                  name='block3_conv1', trainable=False)(net)
net = BatchNormalization()(net)
net = layers.Conv2D(256, (3, 3),
                  activation='relu',
                  padding='same',
                  name='block3_conv2')(net)
net = BatchNormalization()(net)
net = layers.Conv2D(256, (3, 3),
                  activation='relu',
                  padding='same',
                  name='block3_conv3', trainable=False)(net)
net = BatchNormalization()(net)
net = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(net)

# Block 4
net = layers.Conv2D(512, (3, 3),
                  activation='relu',
                  padding='same',
                  name='block4_conv1', trainable=False)(net)
net = BatchNormalization()(net)
net = layers.Conv2D(512, (3, 3),
                  activation='relu',
                  padding='same',
                  name='block4_conv2', trainable=False)(net)
net = BatchNormalization()(net)
net = layers.Conv2D(512, (3, 3),
                  activation='relu',
                  padding='same',
                  name='block4_conv3', trainable=False)(net)
net = BatchNormalization()(net)
net = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(net)

# Block 5
net = layers.Conv2D(512, (3, 3),
                  activation='relu',
                  padding='same',
                  name='block5_conv1', trainable=False)(net)
net = BatchNormalization()(net)
net = layers.Conv2D(512, (3, 3),
                  activation='relu',
                  padding='same',
                  name='block5_conv2', trainable=False)(net)
net = BatchNormalization()(net)
net = layers.Conv2D(512, (3, 3),
                  activation='relu',
                  padding='same',
                  name='block5_conv3', trainable=False)(net)
net = BatchNormalization()(net)


"""
net = layers.Conv2D(100, (3, 3),
                  activation='relu',
                  padding='same',
                  name='blockA_conv1')(net)

net = layers.Conv2D(100, (3, 3),
                  activation='relu',
                  padding='same',
                  name='blockA_conv2')(net)

net = layers.Conv2D(100, (3, 3),
                  activation='relu',
                  padding='same',
                  name='blockA_conv3')(net)


net = layers.Conv2D(100, (15, 15),
                  activation='relu',
                  padding='same',
                  name='blockA_conv4')(net)
"""

net = layers.Conv2D(100, (15, 15),
                  activation='relu',
                  padding='same',
                  name='blockA_conv5')(net)



net = layers.Conv2D(100, (5, 5),
                  activation='relu',
                  padding='same',
                  name='blockB_conv1')(net)

net = layers.Conv2D(50, (3, 3),
                  activation='relu',
                  padding='same',
                  name='blockB_conv2')(net)

net = layers.Conv2D(20, (3, 3),
                  activation='softmax',
                  padding='same',
                  name='blockB_conv3')(net)

model = Model(input_image, net)

model.load_weights('classifier_august/Classifier20epoch.h5',by_name=True)

optimizer = SGD(lr=0.1, decay=0.0, momentum=0.9)

model.compile(loss=ultimate_loss, optimizer=optimizer, metrics=['accuracy'])

model.fit(x=X, y=Y, batch_size=42, epochs=1, verbose=1)

model.fit(X, Y, batch_size=42, epochs=5)

model.fit(X, Y, batch_size=42, epochs=5)

model.fit(X, Y, batch_size=42, epochs=5)

#model.save_weights('18*18_Classifier16epoch.h5')

model.fit(X, Y, batch_size=42, epochs=5)

model.fit(X, Y, batch_size=42, epochs=5)

model.fit(X, Y, batch_size=42, epochs=5)

#model.save_weights('18*18_Classifier31epoch.h5')

ls

