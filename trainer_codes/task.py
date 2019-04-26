#!/usr/bin/python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from . import model

import tensorflow as tf
import argparse
import os

#1
from tensorflow.python.saved_model import builder as saved_builder
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.saved_model import signature_constants

#2
from tensorflow.contrib.training.python.training import hparam

BUCKET_NAME = 'backup-test1'

#PATH = 'gs://' + BUCKET_NAME + '/jobs/humans/'
#PATH_SUB_IMAGES = 'data/'
PATH = '/home/dsepulveda/test_cloud_python/img-20190208T175203Z-001/img/'
PATH_SUB_IMAGES = 'sub_images/'
PATH_TRAIN = 'train/'
PATH_TEST = 'test/'

BATCH_SIZE = 16


def to_savedmodel(model, export_path):
	"""Convert the Keras HDF5 model into TensorFlow SavedModel."""

	builder = saved_builder.SavedModelBuilder(export_path)

	signature = predict_signature_def(inputs={'input': model.inputs[0]}, outputs={'income': model.outputs[0]})

	with tf.keras.backend.get_session() as sess:
		builder.add_meta_graph_and_variables(sess=sess,
											 tags=[tag_constants.SERVING],
											 signature_def_map={signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY: signature})
		builder.save()

def train_and_eval(args):

	tf_keras_model = model.create_model()


	train_settings = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255,
																shear_range=0.2,
																zoom_range=0.2,
																horizontal_flip=True)

	test_settings = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)


	#os.system('mkdir data/')
	#os.system('mkdir data/train/')
	#os.system('mkdir data/test/')

	#gsutil_comand_to_set_train = 'gsutil cp -r ' + 'gs://backup-test1/jobs .'
	#gsutil_comand_to_set_test =  'gsutil cp -r ' + args.test_files + ' data'

	#os.system('cd data \ ls')

	#os.system('ls')
	#os.system('cd ..')

	#os.system(gsutil_comand_to_set_train)
	#os.system(gsutil_comand_to_set_test)

	train_flow = train_settings.flow_from_directory(args.train_files,
													target_size=(100,100),
													batch_size=BATCH_SIZE,
													class_mode = 'binary')

	#print train_flow

	test_flow = test_settings.flow_from_directory(args.test_files,
												   target_size=(100,100),
												   batch_size=BATCH_SIZE,
												   class_mode = 'binary')

	tf_keras_model.fit_generator(generator=train_flow,
				        validation_data=test_flow,
				        epochs=2,
				        steps_per_epoch=2000 // BATCH_SIZE,
				        validation_steps=800 // BATCH_SIZE)

	#tf_keras_model.save_weights('weights_model.hdf5')
	#tf_keras_model.save('model.hdf5')
	#to_savedmodel(tf_keras_model,os.path.join(args.job_dir,'export'))
	export_path = tf.contrib.saved_model.save_keras_model(tf_keras_model, os.path.join(args.job_dir, 'keras_export'))
	export_path = export_path.decode('utf-8')
	print('Model exported to: ', export_path)


if __name__ =='__main__':

	parse = argparse.ArgumentParser()
	parse.add_argument(
		'--train-files',
		help='GCs file path to train data',
		nargs='+',
		default=PATH + PATH_SUB_IMAGES + PATH_TRAIN
		)
	parse.add_argument(
		'--test-files',
		help='GCs file path to test data',
		nargs='+',
		default=PATH + PATH_SUB_IMAGES + PATH_TEST
		)
	parse.add_argument(
    	'--job-dir',
    	type=str,
    	help='GCS or local dir to write checkpoints and export model',
		default='/home/dsepulveda/test_cloud_python/output/')
	parse.add_argument(
        '--verbosity',
        choices=['DEBUG', 'ERROR', 'FATAL', 'INFO', 'WARN'],
        default='INFO')

	arguments,_ = parse.parse_known_args()
	tf.logging.set_verbosity(arguments.verbosity)


	train_and_eval(arguments)