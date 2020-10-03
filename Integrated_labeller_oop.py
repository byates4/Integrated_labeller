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

import Folder_select_GUI as upload
import convert2train_val_sets as tsets
import Labeller_GUI3 as labelgui
import s3_saver
import os


LARGE_FONT = ("Verdana", 12)

class IntegratedLabeller(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        
        container.pack(side="top", fill='both', expand= True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, labellerPage, tsetPage):
        
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
 
 
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="DeepWalk Integrated Viewer", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        img = ImageTk.PhotoImage(Image.open('Labeller_logo.png'))
        
        start_image = tk.Label(self, image=img)
        start_image.image = img
        start_image.pack()
        
        
        butt_upload = tk.Button(self,text ="Upload Images",command = lambda: upload.folder_select()).pack()
        butt_label = tk.Button(self,text ="Label Images",command = lambda: controller.show_frame(labellerPage)).pack()
        butt_sets = tk.Button(self,text ="Create Training and Validation Sets",command = lambda: controller.show_frame(tsetPage)).pack()
        
class labellerPage(tk.Frame):
    def __init__(self, parent, controller):
        global imnum, panel, labellist, ramp
        tk.Frame.__init__(self, parent)
        '''
        tk.title("Join")
        tk.geometry("3000x3000")
        tk.configure(background='grey')
        '''
        labelgui.s32local('unlabelledimages1', 'Temp_S3store/' )
            
        ramp = tk.IntVar()
        ramp.set(1)
        
        labellist = []
        print(os.getcwd())
        filenames = labelgui.create_filelist()
        print(filenames)
        
        imnum = len(filenames) #number of unlabelled images
    
        print(os.getcwd())
        resized = labelgui.resize(filenames[-1])
        #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
        img = ImageTk.PhotoImage(resized)
        #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        
        panel = tk.Label(self, image = img)
        panel.image = img
        panel.pack()
        print(filenames)
        
        tk.Radiobutton(self, text="blended transition", variable = ramp, value=4,indicatoron = 0).pack()
        tk.Radiobutton(self, text="perpendicular", variable = ramp, value=2,indicatoron = 0).pack()
        tk.Radiobutton(self, text="parallel", variable = ramp, value=3, indicatoron = 0).pack()
        tk.Radiobutton(self, text="no ramp", variable = ramp, value=6, indicatoron = 0).pack()
        tk.Radiobutton(self, text="?", variable = ramp, value=5, indicatoron = 0).pack()
        tk.Button(self, text="OK", command = lambda: self.chng(filenames[imnum-1]) ).pack()
        tk.Button(self, text = "Done Labelling", command = lambda: [labelgui.upload2s3(labellist, filenames), controller.show_frame(StartPage) ] ).pack()
        

        
    
    def chng(self, filename):
        sized = labelgui.resize(filename)
        photo2 = ImageTk.PhotoImage(sized)
        panel.config(image = photo2) 
        panel.photo_ref = photo2 # keep a reference
        global imnum, labellist, ramp
        imnum -= 1
        labellist.append(ramp.get())
        print(labellist)

    def done_label(self, filenames):
        IntegratedLabeller.controller.show_frame(StartPage)
        labelgui.upload2s3(labellist, filenames)
    
class tsetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Training Set Conversion", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.data_dir = ''
        
        tk.Button(self,text='Download Files to Local', command= lambda: self.download_set2local()).pack()
        tk.Button(self, text= 'Convert Files to Training set', command= lambda: tsets.create_sets(.2, self.data_dir)).pack()
        
    def download_set2local(self):
        [self.data_dir, image_count] = s3_saver.s3classes2local()

        
        
        
if __name__ == "__main__":
    # execute only if run as a script           
    app = IntegratedLabeller()
    app.mainloop()