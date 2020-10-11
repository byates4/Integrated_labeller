# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 12:08:48 2020

@author: bcyat
"""

from tkinter import Tk
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
        s3_client.upload_file(file_name, bucket, object_name) #upload file to designated s3 bucket
    except ClientError as e:
        logging.error(e)
        return False
    return True

def folder_select():
    #get image directory
    root = Tk()
    og_dir = os.getcwd() #store original directory
    root.directory = filedialog.askdirectory() #brings up tkinter file dialog window
    directory_in_str = root.directory #gets directory name as string
    directory = os.fsencode(directory_in_str) #converts directory to actual file path
    
    
    os.chdir(directory_in_str) #change to selected directory
    for file in os.listdir(directory): #look through files in selected directory
         filename = os.fsdecode(file)
         
         if filename.endswith(".jpg") or filename.endswith(".png"): #check that it's an image
             upload_file(filename, "unlabelledimages1") #upload file to s3 bucket
             continue
         else:
             continue
    os.chdir(og_dir) #change back to original directory
    
    root.mainloop()



