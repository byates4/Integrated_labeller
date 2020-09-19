# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:03:15 2020

@author: bcyat
"""

import tensorflow as tf

import s3_saver

def create_sets(data_dir, validation_split):
    
    batch_size = 32
    img_height = 180
    img_width = 180
    
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
      data_dir,
      validation_split=0.2,
      subset="validation",
      seed=123,
      image_size=(img_height, img_width),
      batch_size=batch_size)

    #identify class names
    class_names = train_ds.class_names
    print(class_names)
    
    return [train_ds,val_ds,class_names]

data_dir = s3_saver.s3classes2local()
train_set, val_set, class_list = create_sets(data_dir, .2)
s3_saver.delete_all_temps()

