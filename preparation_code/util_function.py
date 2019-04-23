#!/usr/bin/python

from os import listdir
from os.path import isfile, join

import numpy as np

from random import randint
from PIL import Image

PATH = '/home/dsepulveda/test_cloud_python/img-20190208T175203Z-001/img/'
PATH_SUB_IMAGES = 'sub_images/'
PATH_TRAIN = 'train/'
PATH_TEST = 'test/'
PATH_CLASS_HUMAN = 'human/'
PATH_CLASS_NO_HUMAN = 'no_human/'

TEST_SIZE = 0.3

XWIDTH = 100
YWIDTH = 100

XLIM = 830
YLIM = 550

def ls(ruta = '.'):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]

def dict_by_filename_image(dict_reader,name_column,image):
	dict_by_filename_image = {}
	i = 0
	for iterator in range(len(dict_reader)):
		if dict_reader[iterator]['filename'] == image:
			dict_by_filename_image[image + '_%d'%i] = int(dict_reader[iterator][name_column])
			i+=1
	return dict_by_filename_image

def column_dic_by_filename(dict_reader,name_column,images):
	dict2_by_filename = {}
	for image in images:
		dict2_by_filename[image] = dict_by_filename_image(dict_reader,name_column,image)
	return dict2_by_filename

def load_images(images):
	imgs = []
	for image in images:
		imgs.append(Image.open(PATH + image))

	return imgs

def imgs_to_arrays(imgs):
    arrays=[]
    for img in imgs:
    	arrays.append(np.array(img))

    return arrays

def arrays_to_imgs(arrays):
	imgs = []
	for array in arrays:
		imgs.append(Image.fromarray(array))

	return imgs

def save_images(imgs,image,train_or_validation_folder,class_folder):
	iterator = 0
	for img in imgs:
		img.save(PATH + PATH_SUB_IMAGES + train_or_validation_folder + class_folder + '%d_'%iterator + image)
		iterator+=1

def random_limits():
	xmin = randint(0,XLIM-XWIDTH)
	xmax = xmin + XWIDTH
	ymin = randint(0,YLIM-YWIDTH)
	ymax = ymin + YWIDTH
	return xmin,xmax,ymin,ymax

def dict_crops(images,xmin,xmax,ymin,ymax):
	j=0
	imgs = load_images(images)
	arrays = imgs_to_arrays(imgs)
	dict_img = {}
	dict_imgR = {}

	for image in images:
		img_list = []
		img_listR = []
		for i in range(len(xmin[image])):
			x_min = xmin[image][image + '_%d'%i]
			x_max = xmax[image][image + '_%d'%i]
			y_min = ymin[image][image + '_%d'%i]
			y_max = ymax[image][image + '_%d'%i]

			x_minR, x_maxR, y_minR, y_maxR = random_limits()

			img_list.append(arrays[j][y_min:y_max,x_min:x_max,:])
			img_listR.append(arrays[j][y_minR:y_maxR,x_minR:x_maxR,:])
	
		j+=1
		dict_img[image] = img_list
		dict_imgR[image] = img_listR
	return dict_img,dict_imgR

def split_train_test(data): 
	size_data = float(len(data))
	size_test = int(size_data*TEST_SIZE)
	test = []
	train = []
	for i in range(int(size_data)):
		if i<=size_test:
			test.append(data[i])
		else:
			train.append(data[i])
	return train,test

def save_array_to_image(cropsH,cropsNH,images):

	for image in images:
		cropH_train,cropH_test = split_train_test(cropsH[image])

		imgs_cropH_train = arrays_to_imgs(cropH_train)
		imgs_cropH_test = arrays_to_imgs(cropH_test)

		save_images(imgs_cropH_train,image,PATH_TRAIN,PATH_CLASS_HUMAN)
		save_images(imgs_cropH_test,image,PATH_TEST,PATH_CLASS_HUMAN)

		cropNH_train,cropNH_test = split_train_test(cropsNH[image])

		imgs_cropNH_train = arrays_to_imgs(cropNH_train)
		imgs_cropNH_test = arrays_to_imgs(cropNH_test)

		save_images(imgs_cropNH_train,image,PATH_TRAIN,PATH_CLASS_NO_HUMAN)
		save_images(imgs_cropNH_test,image,PATH_TEST,PATH_CLASS_NO_HUMAN)