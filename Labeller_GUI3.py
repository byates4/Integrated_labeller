# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 13:08:57 2020

@author: bcyat
"""

import tkinter

from tkinter import Tk
from tkinter import *

import boto3
from PIL import ImageTk,Image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os

def resize(filename):      
    image = str(filename)
    print(filename)
    imgsize = Image.open(image).getbbox()
    divisor = int(imgsize[3])
    imgsize1 = int(imgsize[2])/divisor*500
    size = (int(imgsize1), 500)
    print(size)
    imagebig = Image.open(image).resize(size)
    return imagebig

def chng(filename):
    sized = resize(filename)
    photo2 = ImageTk.PhotoImage(sized)
    panel.config(image = photo2) 
    panel.photo_ref = photo2 # keep a reference
    global imnum, labellist, ramp
    imnum -= 1
    labellist.append(ramp.get())
    Label(window, image= photo2)    

def s32local(s3_bucket, local_path):
    #initiate s3 resource
    s3 = boto3.resource('s3')
    
    # select bucket
    my_bucket = s3.Bucket(s3_bucket)
    
    # download images to temp directory
    os.chdir(local_path)
    for s3_object in my_bucket.objects.all():
        # Need to split s3_object.key into path and file name, else it will give error file not found.
        path, filename = os.path.split(s3_object.key)
        my_bucket.download_file(s3_object.key, filename)

def create_filelist(local_path):
    filenames = [] 
        #main loop iterating through images in temp file
    for file in os.listdir(local_path):
         filename = os.fsdecode(file)
         if filename.endswith(".jpg") or filename.endswith(".png"):
             filenames.append(filename)
             continue
         else:
             continue
    return filenames

def upload2s3(labellist, filenames): 
    s3_client = boto3.client('s3')
            
    for f in range(len(filenames)):
        if labellist[f] == 2:
            response = s3_client.upload_file(filenames[f], 'labelled2', 'perpendicular/{}'.format(filenames[f]))
            print(filenames[f] + ' is perpendicular')
        if labellist[f] == 3:
            response = s3_client.upload_file(filenames[f], 'labelled2', 'parallel/{}'.format(filenames[f]))
            print(filenames[f]+' is parallel')
        if labellist[f] == 4:
            response = s3_client.upload_file(filenames[f], 'labelled2', 'blended_transition/{}'.format(filenames[f]))
            print(filenames[f]+' is a blended transition')
        if labellist[f] == 5:
            response = s3_client.upload_file(filenames[f], 'labelled2', 'not_a_sidewalk/{}'.format(filenames[f]))
            print(filenames[f]+' is fucked up')            
        if labellist[f] == 6:
            response = s3_client.upload_file(filenames[f], 'labelled2', 'no_ramp/{}'.format(filenames[f]))
            print(filenames[f]+' does not have a ramp')

            
def Delete_temps(local_path):
    filelist = [ f for f in os.listdir(local_path) ]
    for f in filelist:
        os.remove(os.path.join(local_path, f))
 
    
s32local('unlabelledimages','C:/Users/bcyat/Documents/Temp_S3store' )
window = Tk()

window.title("Join")
window.geometry("3000x3000")
window.configure(background='grey')


filenames = create_filelist('C:/Users/bcyat/Documents/Temp_S3store')
imnum = len(filenames) #number of unlabelled images


resized = resize(filenames[0])
#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
img = ImageTk.PhotoImage(resized)
#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
panel = Label(window, image = img)

panel.pack(side = "bottom", fill = "both", expand = "yes")

ramp = IntVar()
ramp.set(1)

labellist = [] 

Radiobutton(window, text="blended transition", variable = ramp, value=4,indicatoron = 0).pack()
Radiobutton(window, text="perpendicular", variable = ramp, value=2,indicatoron = 0).pack()
Radiobutton(window, text="parallel", variable = ramp, value=3, indicatoron = 0).pack()
Radiobutton(window, text="no ramp", variable = ramp, value=6, indicatoron = 0).pack()
Radiobutton(window, text="?", variable = ramp, value=5, indicatoron = 0).pack()
Button(window, text="OK", command = lambda: chng(filenames[imnum-1])).pack()

       
window.mainloop()
    
upload2s3(labellist,filenames)

Delete_temps('C:/Users/bcyat/Documents/Temp_S3store')    
