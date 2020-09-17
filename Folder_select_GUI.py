# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 12:08:48 2020

@author: bcyat
"""

import tkinter

from tkinter import Tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog

import boto3

import logging
from botocore.exceptions import ClientError
import os


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


#get image directory
root = Tk()
root.directory = filedialog.askdirectory()
Image_dir = root.directory
print(Image_dir)
directory_in_str = Image_dir

#add images to s3
directory = os.fsencode(directory_in_str)






os.chdir(directory_in_str)
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     
     if filename.endswith(".jpg") or filename.endswith(".png"): 
         filepath = os.path.join(directory_in_str, filename)
         print(filepath)
         upload_file(filename, "unlabelledimages")
         continue
     else:
         continue

root.mainloop()



