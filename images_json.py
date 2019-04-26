#!/usr/bin/python

from __future__ import print_function

import argparse
import base64
from cStringIO import StringIO
import json
import sys

from os import listdir
from os.path import isfile, join, dirname

from PIL import Image

PATH = '/home/dsepulveda/test_cloud_python/img-20190208T175203Z-001/img/'
PATH_SUB_IMAGES = 'sub_images/'
PATH_TRAIN = 'train/'
PATH_TEST = 'test/'
PATH_CLASS_HUMAN = 'human/'
PATH_CLASS_NO_HUMAN = 'no_human'

def ls(ruta = '.'):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]

DESIRED_WITH = 199
DESIRED_HEIGHT = 199


def make_request_json(input_path,input_images, output_json, do_resize):

  with open(output_json, 'w') as ff:
  	for image_handle in input_images:
		# Uses argparse to check permissions, but ignore pre-opened file handle.
		image = Image.open(input_path + image_handle)
		resized_handle = StringIO()
		is_too_big = ((image.size[0] * image.size[1]) >
		            (DESIRED_WITH * DESIRED_HEIGHT))
		if do_resize and is_too_big:
			image = image.resize((199, 199), Image.BILINEAR)

		image.save(resized_handle, format='JPEG')
		encoded_contents = base64.b64encode(resized_handle.getvalue())

		# key can be any UTF-8 string, since it goes in a HTTP request.
		row = json.dumps({'key': image_handle,
		                'image_bytes': {'b64': encoded_contents}})

		ff.write(row)
		ff.write('\n')

  print('Wrote {} images to {}'.format(len(input_images), output_json))


if __name__ == '__main__':

  parser = argparse.ArgumentParser()
  parser.add_argument('-o', '--output',
  					  default='request.json',
                      help='Output file to write encoded images to.')
  parser.add_argument('-r', '--resize',
  					  dest='resize', action='store_true',
                      help='Will resize images locally first.')
  parser.add_argument('--inputs', 
  					  default=PATH + PATH_SUB_IMAGES + PATH_TEST + PATH_CLASS_HUMAN,
  					  nargs='+', 
                      help='A list of .jpg or .jpeg files to serialize into a request json')

  args,_ = parser.parse_known_args()

  input_list = ls(args.inputs)
  input_path = dirname(args.inputs) + '/'


  make_request_json(input_path,input_list, args.output, args.resize)
