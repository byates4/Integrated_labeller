# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:03:15 2020

@author: bcyat
"""

import tensorflow as tf
import os
import s3_saver

def create_sets(validation_split, data_dir):
    '''Creates tensorflow keras training set from directory of
    images stored in folders by class name, validation_split should
    be value between 0-1 and data_dir should be a string'''
    data_dir = 'Temp_class_store/'
    
    #Training set Parameters
    batch_size = 32
    img_height = 180
    img_width = 180
    
    #create training set
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split= validation_split,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)
    
    #create Validation set
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
      data_dir,
      validation_split= validation_split,
      subset="validation",
      seed=123,
      image_size=(img_height, img_width),
      batch_size=batch_size)

    #identify class names
    class_names = train_ds.class_names
    print(class_names)
    print('training and validation sets are preprocessed')
    s3_saver.delete_class_temps() #delete all locally stored files
    
    return [train_ds,val_ds,class_names]





