#!/usr/bin/python

from google.cloud import storage
from os import listdir
from os.path import isfile, join

import sys

BUCKET_ID = 'backup-test1'


def ls(ruta = '.'):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]

def make_blob_public(blob):
    #Makes a blob publicly accessible
    blob.make_public()

    #print('Blob {} is publicly accessible at {}'.format(
    #    blob.name, blob.public_url))


# Check arguments
if len(sys.argv) < 4:
  print 'Usage: ' + sys.argv[0] + ' FILENAME'
  quit()

local_path = sys.argv[1]
#filename = sys.argv[2]
remote_path = sys.argv[2]
public = sys.argv[3]

client = storage.Client()
bucket = client.get_bucket(BUCKET_ID)

data = ls(local_path)

for i in range(len(data)):
	#file name in the bucket (remote)
    blob2 = bucket.blob(remote_path + data[i])
    #local file name to upload
    blob2.upload_from_filename(filename=local_path + data[i])
    if public == 'public':
    	make_blob_public(blob2)