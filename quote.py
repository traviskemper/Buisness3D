#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 11:00:07 2017


@author: Travis Kemper
@email: travis.kemper.w@gmail.com

"""

from Tkinter import Tk, Label, Button
import tkFileDialog
#import numpy
from stl import mesh


class QuoteTool:
    def __init__(self, master):
        self.master = master
        master.title("Quote Tool")

        self.READSTLS = Button(master, text="Add STL to Order", command=self.read_stls)
        self.READSTLS.pack()
        
        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

      
    def read_stls(self):
        #surf_areas = numpy.zeros(3)
        filenames_str = tkFileDialog.askopenfilenames(filetypes=[("*.STL","*.stl")])
        for stl_file in list(filenames_str):
            part_name = stl_file.split("/")[-1].replace(".STL","")
            part_mesh = mesh.Mesh.from_file(stl_file)
            self.label = Label(self.master, text="Reading {} ".format(part_name))
            self.label.pack()
        
root = Tk()
my_gui = QuoteTool(root)
root.mainloop()