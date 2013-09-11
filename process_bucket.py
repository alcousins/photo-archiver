#!/usr/bin/python

import boto
from boto.s3.key import Key
from PIL import Image
import sys, os, glob


input_bucket_names = ['acousins-photos-store']
thumbnails_bucket_name = 'acousins-photos-thumbnails'
tempfilename = '/tmp/photo-archiver-tmpfile'
thumbnail_size = 960, 640

conn = boto.connect_s3()

try: 
  output_bucket = conn.get_bucket(thumbnails_bucket_name)
except boto.exception.S3ResponseError:
  print "Ooops, thumbnail bucket " + thumbnails_bucket_name + " doesn't exist?"

for b in input_bucket_names: 
  try: 
    input_bucket = conn.get_bucket(b)
    keys = input_bucket.list()
    for i in keys:
      print "Processing: " + i.key

      prefix, ext = os.path.splitext(i.key)

      i.get_contents_to_filename(tempfilename)
      print "Downloaded"
      im = Image.open(tempfilename)
      im.thumbnail(thumbnail_size, Image.ANTIALIAS)
      print "Thumbnailed"
      im.save(tempfilename + "_small", "JPEG")
      print "Saved"
      tk = Key(output_bucket)
      tk.key = prefix + '_small' + ext
      print "Key Created"
      tk.set_contents_from_filename(tempfilename + "_small")
      print "Uploaded"
  except boto.exception.S3ResponseError as e:
    print "Ooops, bucket " + b + " doesn't exist?"
    print e
