#!/usr/bin/python

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense

BUCKET_NAME = 'backup-test1'

#PATH = 'gs://' + BUCKET_NAME + '/jobs/humans/'
#PATH_SUB_IMAGES = 'data/'
PATH = '/home/dsepulveda/test_cloud_python/img-20190208T175203Z-001/img/'
PATH_SUB_IMAGES = 'sub_images/'
PATH_TRAIN = 'train/'
PATH_TEST = 'test/'

BATCH_SIZE = 4

def ls(ruta = '.'):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(100, 100, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])

#img_names_train = ls(PATH + PATH_SUB_IMAGES + PATH_TRAIN)
#img_names_test = ls(PATH + PATH_SUB_IMAGES + PATH_TEST)

train_settings = ImageDataGenerator(rescale=1./255,
									shear_range=0.2,
									zoom_range=0.2,
									horizontal_flip=True)

test_settings = ImageDataGenerator(rescale=1./255)

train_flow = train_settings.flow_from_directory(PATH + PATH_SUB_IMAGES + PATH_TRAIN,
												target_size=(100,100),
												batch_size=BATCH_SIZE,
												class_mode = 'binary')

#print train_flow

test_flow = train_settings.flow_from_directory(PATH + PATH_SUB_IMAGES + PATH_TEST,
											   target_size=(100,100),
											   batch_size=BATCH_SIZE,
											   class_mode = 'binary')

model.fit_generator(generator=train_flow,
			        validation_data=test_flow,
			        epochs=2,
			        steps_per_epoch=2000 // BATCH_SIZE,
			        validation_steps=800 // BATCH_SIZE)

model.save_weights('weights_model.h5')
model.save('model.h5')




