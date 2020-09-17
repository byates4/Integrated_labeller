# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:03:15 2020

@author: bcyat
"""

import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras import layers

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

