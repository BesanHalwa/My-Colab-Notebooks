# -*- coding: utf-8 -*-
"""little_classifier0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P6UsTEH3D95sMhucnMFKyCbqkQkWtRZy
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

cd drive

ls

cd pascal_data

ls

import numpy as np

X = np.load('pascalX.npy')
Y = np.load('pascaly.npy')

print(X.shape)
print(Y.shape)

X_val = np.load('pascalX_val.npy')
Y_val = np.load('pascaly_val.npy')

# import modules
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.layers.normalization import BatchNormalization
from keras import optimizers
import keras

x = Sequential()

# Block 1
x.add(Conv2D(64, (1, 1),activation='relu',padding='same',input_shape=(300,300,3)))
x.add(Conv2D(64, (1, 1),activation='relu',padding='same'))
x.add(MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool'))

# Block 2
x.add(Conv2D(64, (2, 2),activation='relu',padding='same'))
x.add(Conv2D(64, (2, 2),activation='relu',padding='same'))
x.add(Conv2D(64, (2, 2),activation='relu',padding='same'))
x.add(Conv2D(64, (2, 2),activation='relu',padding='same'))
x.add(MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool'))
x.add(BatchNormalization())


# Block 3
x.add(Conv2D(128, (2, 2),activation='relu',padding='same'))
x.add(Conv2D(128, (1, 1),activation='relu',padding='same'))

x.add(MaxPooling2D((2, 2), strides=(2, 2)))
x.add(Dropout(0.2))



# Classification block
x.add(Flatten())

# x.add(Dense(1000, activation='relu'))
x.add(Dense(800, activation='relu'))
x.add(Dense(20, activation='softmax', name='predictions'))

# original parameters (lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
sgd = optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)

# original parameters (lr=0.02, beta_1=0.9, beta_2=0.999, epsilon=None, schedule_decay=0.004)
nadam = optimizers.Nadam(lr=0.02, beta_1=0.9, beta_2=0.999, epsilon=None, schedule_decay=0.004)

# original parameters (lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
adam = optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)

# categorical_crossentropy
# mean_squared_error
x.compile(loss='categorical_crossentropy',
              optimizer=adam,
              metrics=['accuracy'])

for i in range(15):
  print("epoch",i+1)
  x.fit(X, Y,epochs=1,batch_size=5,validation_data=(X_val, Y_val))
  x.save('littleClassifier.h5')
  print("----------------------------------------------------------------------")
  print("----------------------------------------------------------------------")

