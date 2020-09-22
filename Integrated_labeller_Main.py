# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 22:46:27 2020

@author: bcyat
"""
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
import sys

import Folder_select_GUI as upload
import convert2train_val_sets as tsets
import Labeller_GUI3 as labelgui

'''
class PrintLogger(): # create file like object
    def __init__(self, textbox): # pass reference to text widget
        self.textbox = textbox # keep ref

    def write(self, text):
        self.textbox.insert(END, text) # write text to textbox
            # could also scroll to end of textbox here to make sure always visible

    def flush(self): # needed for file like object
        pass
'''

def main():
    root = Toplevel()
    root.geometry = ("500x500")
    label = Label(root, text ="Welcome to the DeepWalk Integrated Labeller") 
    label.pack(pady = 10) 
    img = ImageTk.PhotoImage(Image.open('Labeller_logo.png'))

    #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    Label(root, image = img).pack()  
    # a button widget which will open a  
    # new window on button click 
    btn = Button(root,text ="Upload Images",command = lambda: upload.folder_select()).pack()
    btn2 = Button(root,text ="Label Images",command = lambda: labelgui.labeller()).pack()
    btn3 = Button(root,text ="Create Training and Validation Sets",command = lambda:tsets.create_sets(.2)).pack()
    # create instance of file like object
    '''
    t = Text(root)
    t.pack()
    
    pl = PrintLogger(t)

    # replace sys.stdout with our object
    sys.stdout = pl
    '''
    # mainloop, runs infinitely 
    mainloop() 
        


if __name__ == '__main__':
    main()
