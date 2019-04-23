#!/usr/bin/python

from os import path, mkdir
from shutil import rmtree

PATH = '/home/dsepulveda/test_cloud_python/img-20190208T175203Z-001/img/'
PATH_SUB_IMAGES = 'sub_images/'
PATH_TRAIN = 'train/'
PATH_TEST = 'test/'
PATH_CLASS_HUMAN = 'human/'
PATH_CLASS_NO_HUMAN = 'no_human'

if path.exists(PATH + PATH_SUB_IMAGES):
	rmtree(PATH + PATH_SUB_IMAGES)

mkdir(PATH + PATH_SUB_IMAGES)
mkdir(PATH + PATH_SUB_IMAGES + PATH_TRAIN)
mkdir(PATH + PATH_SUB_IMAGES + PATH_TEST)

mkdir(PATH + PATH_SUB_IMAGES + PATH_TRAIN + PATH_CLASS_HUMAN)
mkdir(PATH + PATH_SUB_IMAGES + PATH_TRAIN + PATH_CLASS_NO_HUMAN)
mkdir(PATH + PATH_SUB_IMAGES + PATH_TEST + PATH_CLASS_HUMAN)
mkdir(PATH + PATH_SUB_IMAGES + PATH_TEST + PATH_CLASS_NO_HUMAN)