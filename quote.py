#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 11:00:07 2017


@author: Travis Kemper
@email: travis.kemper.w@gmail.com

"""

from Tkinter import Tk, Text, Button, END
import tkFileDialog
#import numpy
from stl import mesh


class Part:
    def __init__(self,name):
        self.units = 'mm'
        self.name = name 
        self.mesh = None 
        self.volume = 0.0 
        self.density = 0.00118 # g/mm^3
        self.material_cost = 1.6      # USD/g
        self.sup_density = 0.00117 # g/mm^3
        self.sup_material_cost = 0.6      # USD/g
        self.quantity = 1
        self.cost = {}
        
    def __del__(self):
        """
        Destructor, clears object memory
        """
        del self.units 
        del self.name 
        del self.mesh
        del self.volume
        del self.density
        del self.material_cost
        del self.sup_density
        del self.sup_material_cost
        
        
class QuoteTool:
    def __init__(self, master):
        self.master = master
        self.parts = {}
        
        
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
            part_i = Part(part_name)
            part_i.mesh = mesh.Mesh.from_file(stl_file)
            part_i.volume, cog, inertia = part_i.mesh.get_mass_properties()
            
            part_i.mass = part_i.density*part_i.volume
            part_i.cost['material'] = part_i.mass*part_i.material_cost
            
            self.parts[part_name] = part_i
            self.part_text = Text(self.master,height=1, width=150) 
            self.part_text.pack()
            self.part_text.insert(END,"Reading {} with volume of {} {}^3 a mass of {} and a cost of {} ".format(part_name,part_i.volume, part_i.units,part_i.mass,part_i.cost['material']))
            
            
root = Tk()
my_gui = QuoteTool(root)
root.mainloop()