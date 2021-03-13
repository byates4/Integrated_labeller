# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import boto3
import json
import tifffile as tff
import numpy as np
from PIL import Image
import os





s3_client = boto3.client('s3')
all_objects = s3_client.list_objects_v2(Bucket = 'integrated-labeller-main')
all_objects = all_objects['Contents']
filenames = []

s3 = boto3.resource("s3")
bucket = s3.Bucket('integrated-labeller-main')

d_filenames = []
col_filenames = []

for i in all_objects:
    if i['Key'].endswith('_d.jpg'):
        d_filenames.append(i['Key'])
    elif i['Key'].endswith('.jpg'):
        col_filenames.append(i['Key'])

annotations = {}
count = 0

for filename in col_filenames:
    annotations[filename] = {
        "color_filename":filename,
        "depth_filename":d_filenames[count],
        "label":None,
        "regions":None}
    count += 1

with open('Annotations.json', 'w') as f:
    json.dump(annotations, f)

# =============================================================================
# def convert2jpg(tif):
#     
#     global col_im, im_name
#     dep_im = tff.imread(tif)
#     im_name = tif[0:-5] + '_d' + '.jpg'
#     col_im = dep_im[:,:,3].astype(np.uint8)
#     col_im = col_im[:,:]
#     col_im = Image.fromarray(col_im, mode = 'L')
#     col_im.save(im_name)
# 
# 
# for filename in os.listdir():
#     if filename.endswith(".tif") or filename.endswith(".tiff"): 
#          convert2jpg(filename)
#          continue
#     else:
#         continue
# 
# =============================================================================
# =============================================================================
# for i in all_objects:
#     if i['Key'][-1] == 'f':
#         filenames.append(i['Key'])
#         print('downloading ' + i['Key'])
#         bucket.download_file(i['Key'],i['Key'])
# =============================================================================
        
        
        




