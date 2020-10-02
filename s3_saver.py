"""
Created on Thu Sep 17 09:20:51 2020
@author: bcyat
"""

import os
import boto3

def Delete_temps(local_path):
    filelist = [ f for f in os.listdir(local_path) ]
    for f in filelist:
        os.remove(os.path.join(local_path, f))

def file_list(bucket):
    s3c = boto3.client('s3')
    all_objects = s3c.list_objects_v2(Bucket = bucket)
    all_objects = all_objects['Contents']

    file_list = []
    
    for obj in all_objects:
        key = obj['Key']
        if key[-1] != 'g':
            continue
        file_list.append(key)
    return file_list


def download_s3_folder(bucket_name, filenames):
    """
    Download the contents of a folder directory
    Args:
        bucket_name: the name of the s3 bucket
        s3_folder: the folder path in the s3 bucket
        local_dir: a relative or absolute directory path in the local file system
    """
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    # Directory 
    #directory = '/perpendicular/'  
    # Parent Directory path 
    loc_path = 'Temp_class_store/'
    down_count = 0 
    # Path 
    #os.mkdir(loc_path)
    #print(filenames)
    for s3path in filenames:
        
        '''
        target = obj.key if local_dir is None \
            else os.path.join(local_dir, os.path.basename(obj.key))
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        print(obj.key)
        print(target)
        '''
        down_count += 1
        print(s3path + " is downloaded")
        path = loc_path + s3path
        #print(path)
        try:
            bucket.download_file(s3path, path)
            
        except:
            continue


def s3classes2local():
    bucket = "labelled2"
    filenames = file_list(bucket)
    
    
        
    download_s3_folder('labelled2',filenames)
    return ['Temp_class_store/', len(filenames)]
    
    
def delete_all_temps():   
    Delete_temps('Temp_class_store/perpendicular')
    Delete_temps('Temp_class_store/blended_transition')
    Delete_temps('Temp_class_store/no_ramp')
    Delete_temps('Temp_class_store/not_a_sidewalk')
    Delete_temps('Temp_class_store/parallel')



