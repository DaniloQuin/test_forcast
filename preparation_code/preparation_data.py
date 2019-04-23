#!/usr/bin/python

import csv

from util_function import ls

from util_function import column_dic_by_filename
from util_function import dict_crops
from util_function import save_array_to_image

PATH_IMAGES = '/home/dsepulveda/test_cloud_python/img-20190208T175203Z-001/img/'
PATH_LABELS = '/home/dsepulveda/test_cloud_python/'

images = ls(PATH_IMAGES)

file_labels = open(PATH_LABELS + 'report_labels_2019.csv')
reader = csv.DictReader(file_labels, delimiter=',')
reader = list(reader)

xmin = column_dic_by_filename(reader,'xmin',images)
ymin = column_dic_by_filename(reader,'ymin',images)
xmax = column_dic_by_filename(reader,'xmax',images)
ymax = column_dic_by_filename(reader,'ymax',images)

labels_crops = dict_crops(images,xmin,xmax,ymin,ymax)
save_array_to_image(labels_crops[0],labels_crops[1],images)