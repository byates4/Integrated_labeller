# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:03:15 2020

@author: bcyat
"""

import tensorflow as tf

import s3_saver

def create_sets(validation_split):
    data_dir = s3_saver.s3classes2local()
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
    print('training and validation sets are preprocessed')
    s3_saver.delete_all_temps()
    
    return [train_ds,val_ds,class_names]





