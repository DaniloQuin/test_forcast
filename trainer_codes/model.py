#!/usr/bin/python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import tensorflow as tf

BUCKET_NAME = 'backup-test1'

#PATH = 'gs://' + BUCKET_NAME + '/jobs/humans/'
#PATH_SUB_IMAGES = 'data/'
PATH = '/home/dsepulveda/test_cloud_python/img-20190208T175203Z-001/img/'
PATH_SUB_IMAGES = 'sub_images/'
PATH_TRAIN = 'train/'
PATH_TEST = 'test/'

BATCH_SIZE = 4

def create_model():

	model = tf.keras.Sequential()
	model.add(tf.keras.layers.Conv2D(32, (3, 3), input_shape=(100, 100, 3)))
	model.add(tf.keras.layers.Activation('relu'))
	model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

	model.add(tf.keras.layers.Conv2D(32, (3, 3)))
	model.add(tf.keras.layers.Activation('relu'))
	model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

	model.add(tf.keras.layers.Conv2D(64, (3, 3)))
	model.add(tf.keras.layers.Activation('relu'))
	model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

	model.add(tf.keras.layers.Flatten())  
	model.add(tf.keras.layers.Dense(64))
	model.add(tf.keras.layers.Activation('relu'))
	model.add(tf.keras.layers.Dropout(0.5))
	model.add(tf.keras.layers.Dense(1))
	model.add(tf.keras.layers.Activation('sigmoid'))

	model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])

	return model






