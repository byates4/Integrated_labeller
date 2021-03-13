# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 17:54:17 2020

@author: bcyat
"""
import config
import tkinter as tk
from tkinter.ttk import *
from PIL import ImageTk, Image
import sys
import matplotlib.pyplot as plt

import tensorflow as tf
import Folder_select_GUI as upload
import convert2train_val_sets as tsets
import Labeller_GUI3 as labelgui
import s3_saver
from labelme import __main__ as annotator
import sort_images as sort

import os
import boto3
import json

LARGE_FONT = ("Verdana", 12) #initialize font

class data():
    def __init__(self, *args, **kwargs):
        self.training_set = None
        self.validation_set = None
        self.class_names = None
        self.val_batches = None
        self.test_dataset = None
        self.validation_set = None
        
        
class MLmodel():
    def __init__(self, *args, **kwargs):
        self.IMG_SIZE = (180, 180)
        self.model = None
        
class IntegratedLabeller(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self) 
        
        #make 1x1 grid for windows
        container.pack(side="top", fill='both', expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry("1000x1000") #set default window size
        self.frames = {}
        
        #add page objects to the integratedlabeller class
        for F in (StartPage, labellerPage, tsetPage):
        
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        #raise selected frame to top of window
        frame = self.frames[cont]
        frame.tkraise()
 
 
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="DeepWalk Integrated Viewer", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        img = ImageTk.PhotoImage(Image.open('Labeller_logo.png')) #load home image
        
        #display home image
        start_image = tk.Label(self, image=img)
        start_image.image = img #making copy prevents pyimage# error
        start_image.pack()
        
        def load_ann():
            #Load Annotations
            s3 = boto3.resource("s3")
            bucket_main = s3.Bucket('integrated-labeller-main')
            bucket_main.download_file("Annotations.json","Annotations.json")
            
            with open('Annotations.json') as f:
                data = json.load(f)
            
            for key in data:
                features = data[key]
                if features['regions'] == None:
                    if '/' in features['color_filename']:
                        continue
                    path = 'labelme/images/' + features['color_filename']
                    print(path)
                    bucket_main.download_file(features['color_filename'],path)
        
        butt_upload = tk.Button(self,text ="Upload Images",command = lambda: upload.folder_select(self)).pack()
        butt_label = tk.Button(self,text ="Label Images",command = lambda: [controller.show_frame(labellerPage), labellerPage.setup(self)]).pack()
        butt_sets = tk.Button(self,text ="Create Training and Validation Sets",command = lambda: controller.show_frame(tsetPage)).pack()
        butt_annotate = tk.Button(self, text = 'Annotate Images', command = lambda: [load_ann(), annotator.main()] ).pack()      


class labellerPage(tk.Frame):
    def __init__(self, parent, controller):
        global imnum, panel, labellist, ramp, filenames
        tk.Frame.__init__(self, parent)
        
        
        
        
        resized = labelgui.resize('all_images_labelled.png') #resize and display first image
        #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
        img = ImageTk.PhotoImage(resized)
        #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        
        panel = tk.Label(self, image=img)
        #panel.config(image = img)
        panel.pack()
        panel.photo_ref = img
        
        
        ramp = tk.IntVar()
        ramp.set(1)
        labellist = []
        imnum = 0
        
        try:
            #Never have value = 1
            tk.Radiobutton(self, text="blended transition", variable = ramp, value=4,indicatoron = 0).pack()
            tk.Radiobutton(self, text="perpendicular", variable = ramp, value=2,indicatoron = 0).pack()
            tk.Radiobutton(self, text="parallel", variable = ramp, value=3, indicatoron = 0).pack()
            tk.Radiobutton(self, text="no ramp", variable = ramp, value=6, indicatoron = 0).pack()
            tk.Radiobutton(self, text="?", variable = ramp, value=5, indicatoron = 0).pack()
            tk.Button(self, text="OK", command = lambda: self.chng(filenames, controller) ).pack()
        except:
            print('dangit')
        #tk.Button(self, text = "Done Labelling", command = lambda: [labelgui.upload2s3(labellist, filenames), controller.show_frame(StartPage) ] ).pack()
    def setup(self):
        global filenames, panel
        
        #try:
        sort.sort_images()
        labelgui.s32local('unlabelledimages1', 'Temp_S3store/')
        filenames = labelgui.create_filelist()
        #og_dir = os.getcwd()
        os.chdir('Temp_S3store/')
        print("original imnum" + str(imnum))
        sized = labelgui.resize(filenames[imnum])
        photo2 = ImageTk.PhotoImage(sized)
        panel.config(image = photo2) 
        panel.photo_ref = photo2 # keep a reference
        '''
        except:
            print("No images to label")
        '''    
    def chng(self, filenames, controller):
        global imnum, labellist, ramp
        imnum += 1
        labellist.append(ramp.get())
        #print("labellist" + labellist)
        try:
            sized = labelgui.resize(filenames[imnum])
            photo2 = ImageTk.PhotoImage(sized)
            panel.config(image = photo2) 
            panel.photo_ref = photo2 # keep a reference
            
        except: 
            print('all images are labelled')
            labelgui.upload2s3(labellist, filenames)
            controller.show_frame(StartPage)
            labelgui.clear_temps(filenames)
            labellist = []
            imnum = 0
            os.chdir('..')
   
    
class tsetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Training Set Conversion", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.data_dir = ''
        
        self.training_set = ''
        self.validation_set = ''
        
        tk.Button(self,text='Download Files to Local', command= lambda: self.download_set2local()).pack()
        tk.Button(self, text= 'Convert Files to Training set', command= lambda: self.dev_sets()).pack()
        tk.Button(self, text= 'Home Page', command = lambda: controller.show_frame(StartPage)).pack()
        tk.Button(self, text= 'Print', command = lambda: self.print_state()).pack()
        tk.Button(self, text= 'display', command = lambda: self.test_images()).pack()
        tk.Button(self, text= 'delete local files', command = lambda: s3_saver.delete_class_temps()).pack()
        tk.Button(self, text= 'preprocess', command = lambda: self.preprocess()).pack()
        tk.Button(self, text= 'Data Augmentation', command = lambda: self.data_aug()).pack()
        tk.Button(self, text= 'Build Model', command = lambda: self.create_model()).pack()
        tk.Button(self, text= 'Train Model', command = lambda: self.train_model()).pack()
        
    def download_set2local(self):
        [self.data_dir, image_count] = s3_saver.s3classes2local()
    def dev_sets(self):
        [train_ds,val_ds,class_names] = tsets.create_sets(.2, self.data_dir)
        data.training_set = train_ds
        data.validation_set = val_ds
        data.class_names = class_names
    def test_images(self):
        class_names = data.class_names
        
        plt.figure(figsize=(10, 10))
        for images, labels in data.training_set.take(1):
          for i in range(3):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.title(class_names[labels[i]])
            plt.axis("off")
            
    def print_state(self):
        print(data.training_set)
        print(data.validation_set)
        print(data.class_names)  
    
    def preprocess(self):
        data.val_batches = tf.data.experimental.cardinality(data.validation_set)
        data.test_dataset = data.validation_set.take(data.val_batches // 5)
        data.validation_set = data.validation_set.skip(data.val_batches // 5)
        
        AUTOTUNE = tf.data.experimental.AUTOTUNE

        data.training_set = data.training_set.prefetch(buffer_size=AUTOTUNE)
        data.validation_set = data.validation_set.prefetch(buffer_size=AUTOTUNE)
        data.test_dataset = data.test_dataset.prefetch(buffer_size=AUTOTUNE)
        print(data.training_set)
        print(data.validation_set)
        print(data.class_names)  
        
    def data_aug(self):
        data_augmentation = tf.keras.Sequential([tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal'), tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),])
        for image, _ in data.training_set.take(1):
            plt.figure(figsize=(10, 10))
            first_image = image[0]
        for i in range(3):
            ax = plt.subplot(3, 3, i + 1)
            augmented_image = data_augmentation(tf.expand_dims(first_image, 0))
            plt.imshow(augmented_image[0] / 255)
            plt.axis('off')
        preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input
        rescale = tf.keras.layers.experimental.preprocessing.Rescaling(1./127.5, offset= -1)
        
    def create_model(self):
        # Create the base model from the pre-trained model MobileNet V2
        IMG_SHAPE = (180,180) + (3,) #EDIT hardcoded the image size
        base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,include_top=False,weights='imagenet')
        
        data.image_batch, data.label_batch = next(iter(data.training_set))
        data.feature_batch = base_model(data.image_batch)
        print(data.feature_batch.shape)
        
        base_model.trainable = False
        
        data.global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
        data.feature_batch_average = data.global_average_layer(data.feature_batch)
        print(data.feature_batch_average.shape)
        
        prediction_layer = tf.keras.layers.Dense(1)
        prediction_batch = prediction_layer(data.feature_batch_average)
        print(prediction_batch.shape)
        
        data_augmentation = tf.keras.Sequential([tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal'), tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),])
        preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input
        inputs = tf.keras.Input(shape=(180, 180, 3))
        x = data_augmentation(inputs)
        x = preprocess_input(x)
        x = base_model(x, training=False)
        x = data.global_average_layer(x)
        x = tf.keras.layers.Dropout(0.2)(x)
        outputs = prediction_layer(x)
        model = tf.keras.Model(inputs, outputs)
        
        base_learning_rate = 0.0001
        model.compile(optimizer=tf.keras.optimizers.Adam(lr=base_learning_rate),
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])
        
        MLmodel.model = model
        print(model.summary())
        print(model.trainable_variables)
        
    def train_model(self):
        initial_epochs = 10
        loss0, accuracy0 = MLmodel.model.evaluate(data.validation_set)
        
        print("initial loss: {:.2f}".format(loss0))
        print("initial accuracy: {:.2f}".format(accuracy0))
    
        history = MLmodel.model.fit(data.training_set,
                epochs=initial_epochs,
                validation_data=data.validation_set)
        
        print(history)
        
        
if __name__ == "__main__":
    # execute only if run as a script           
    app = IntegratedLabeller()
    app.mainloop()