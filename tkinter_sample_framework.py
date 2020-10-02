# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 17:54:17 2020

@author: bcyat
"""

import tkinter as tk
from tkinter as ttk

LARGE_FONT = ("Verdana", 12)

class SeaofBTCapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        
        container.pack(side="top", fill='both', expand= True)        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, PageOne, PageTwo):
        
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
 
def qf(param):
     print(param)
 
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        button2 = ttk.Button(self,text="Visit Page 1",command= lambda: controller.show_frame(PageOne))
        button2.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 1", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        button1 = ttk.Button(self,text="Back to Home",command= lambda: controller.show_frame(StartPage))        
        button1.pack()

        
        button6 = tk.Button(self,text="Page 2",command= lambda: controller.show_frame(PageTwo))        
        button6.pack()
        
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 2", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
                
        button4 = ttk.Button(self,text="Page 1",command= lambda: controller.show_frame(PageOne))
        
        button4.pack()
        
        button5 = ttk.Button(self,text="Back to Home",command= lambda: controller.show_frame(StartPage))        
        button5.pack()
        
app = SeaofBTCapp()
app.mainloop()