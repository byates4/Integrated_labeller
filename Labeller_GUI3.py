# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 13:08:57 2020
@author: bcyat
"""


from tkinter import Tk
from tkinter import *

import boto3
from PIL import ImageTk,Image
import os
import tifffile as tff
from matplotlib import cm
import numpy as np

    

def resize(filename):
    ''' resize image and convert to PIL Image object'''      
    if filename[-1] == 'f':
        imtif = tff.imread(filename)
        im = Image.fromarray(np.uint8(imtif[:,:,0:3]))
        imgsize = im.getbbox()
        divisor = int(imgsize[3])
        imgsize1 = int(imgsize[2])/divisor*500
        size = (int(imgsize1), 500)
        imagebig = im.resize(size)
    
    else:
        image = str(filename)
        imgsize = Image.open(image).getbbox()
        divisor = int(imgsize[3])
        imgsize1 = int(imgsize[2])/divisor*500
        size = (int(imgsize1), 500)
        imagebig = Image.open(image).resize(size)
    return imagebig

def s32local(s3_bucket, local_path):
    #initiate s3 resource
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(s3_bucket) #designate s3 bucket
    
    # download images to temp directory
    ogdir = os.getcwd() #store original directory
    #print('FUCK' + ogdir)
    os.chdir(local_path) #set dir for images to be uploaded
    print("Loading Images from S3")
    ob_tot = len(list(my_bucket.objects.all())) #count total images to be uploaded
    im_count = 1
    
    for s3_object in my_bucket.objects.all():
        
        # Need to split s3_object.key into path and file name, else it will give error file not found.
        path, filename = os.path.split(s3_object.key)
        my_bucket.download_file(s3_object.key, filename) #download object as filename
        print("Loaded image " + str(im_count) + " of " + str(ob_tot))
        im_count += 1
    os.chdir(ogdir) #change back to original directory

def create_filelist():
    filenames = [] 
        #main loop iterating through images in temp file
    og_dir = os.getcwd()
    os.chdir('Temp_S3store')
    for file in os.listdir(os.getcwd()): #iterate through directory and collect filenames
         filename = os.fsdecode(file)
         if file.endswith(".jpg") or file.endswith(".png") or file.endswith('tif'):
             filenames.append(filename)
             continue
         else:
             continue
    os.chdir(og_dir)
    return filenames #return list of files to be annotated

def upload2s3(labellist, filenames):
    '''upload labelled images to s3'''
    
    s3_client = boto3.client('s3')
    print(filenames)
    if labellist[0] != 1:
        print(str(len(labellist)) + ' files were labelled')
    
    for f in range(len(filenames)):
        if f+1 > len(labellist): #check that there are still images to upload
            break
        if labellist[f] == 2:
            s3_client.upload_file(filenames[f], 'labelled1', 'perpendicular/{}'.format(filenames[f]))
            s3_client.delete_object(Bucket = 'unlabelledimages1', Key = filenames[f])
            print(filenames[f] + ' is perpendicular')
        if labellist[f] == 3:
            s3_client.upload_file(filenames[f], 'labelled1', 'parallel/{}'.format(filenames[f]))
            s3_client.delete_object(Bucket = 'unlabelledimages1',Key = filenames[f])
            print(filenames[f]+' is parallel')
        if labellist[f] == 4:
            s3_client.upload_file(filenames[f], 'labelled1', 'blended_transition/{}'.format(filenames[f]))
            s3_client.delete_object(Bucket = 'unlabelledimages1', Key = filenames[f])
            print(filenames[f]+' is a blended transition')
        if labellist[f] == 5:
            s3_client.upload_file(filenames[f], 'labelled1', 'not_a_sidewalk/{}'.format(filenames[f]))
            s3_client.delete_object(Bucket = 'unlabelledimages1', Key = filenames[f])
            print(filenames[f]+' is fucked up')            
        if labellist[f] == 6:
            s3_client.upload_file(filenames[f], 'labelled1', 'no_ramp/{}'.format(filenames[f]))
            s3_client.delete_object(Bucket = 'unlabelledimages1', Key = filenames[f])
            print(filenames[f]+' does not have a ramp')
        
            
def clear_temps(filenames):
    for f in filenames:
        if f[-1] == 'g' or 'f':
            print('deleting ' + f)
            os.remove(f)
