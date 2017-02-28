#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 11:00:07 2017


@author: Travis Kemper
@email: travis.kemper.w@gmail.com

"""

from Tkinter import Tk
import Tkinter as tk #, Text, Button, END, BOTTOM
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
        # Lines of part table
        self.labels_part_names = {}
        self.labels_part_quantities = {}        
        self.warnings = {}
        
        self.n_parts = 0
        self.column_width = {}
        self.total_cost = 0.0 
        
        
        
        master.title("Quote Tool")
        
        column_name = "Parts"
        self.column_width[column_name] = 120
        self.part_list_label = tk.Label(master,text=column_name,height=1, width=self.column_width[column_name])
        self.part_list_label.grid(row=0,column=0)
        
        
        self.part_q_label = tk.Label(master,text="Quantity",height=1, width=10)
        self.part_q_label.grid(row=0,column=1)

        self.warnings_label = tk.Label(master,text="",height=1, width=10)
        self.warnings_label.grid(row=0,column=2)

        
        self.update = tk.Button(master,text="Update",command=self.update_quantity)
        
        self.READSTLS = tk.Button(self.master, text="+", command=self.read_stls)
        self.order_value = tk.Label(self.master,height=1, width=self.column_width["Parts"])
        
        self.display_footer()
        
    def display_footer(self):
        
        self.n_parts = len(self.parts)
        
        self.READSTLS.grid(row=self.n_parts+1,column=0)
        
        self.update.grid(row=self.n_parts+2,column=1)
        
        self.order_value.config(text='Order ${:.2f} '.format(self.total_cost))
        self.order_value.grid(row=self.n_parts+2,column=0)
           
        
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
            
        self.display_parts()
        
    def grid_parts(self):
        part_n = 1
        for part_key,part_i in self.parts.iteritems():
            self.labels_part_names[part_key].grid(row=part_n,column=0)
            self.labels_part_quantities[part_key].grid(row=part_n,column=1)
            self.warnings[part_key].grid(row=part_n,column=2)
                                          
            part_n += 1
            
    def display_parts(self):
        part_n = 1
        for part_key,part_i in self.parts.iteritems():
            
            self.labels_part_names[part_key] = tk.Label(self.master,height=1,width=self.column_width["Parts"],text="Reading {} with volume of {:.3f} {}^3 a mass of {:.2f} g and a cost of ${:.2f} ".format(part_i.name,part_i.volume, part_i.units,part_i.mass,part_i.cost['material'])) 
            self.labels_part_names[part_key].grid(row=part_n,column=0)
            #self.part_text.insert(tk.END,)
            #self.part_q = tk.Entry("1")
            #self.part_q.grid(row=self.n_parts,column=2)
            # Show quantity 
            self.labels_part_quantities[part_key] = tk.Entry(self.master)
            self.labels_part_quantities[part_key].insert(tk.END,part_i.quantity)
            self.labels_part_quantities[part_key].grid(row=part_n,column=1)
                                        
            # Add blank warning column
            self.warnings[part_key] = tk.Label(self.master,text="",fg="red")
            self.warnings[part_key].grid(row=part_n,column=2)
                                          
            part_n += 1
        self.grid_parts()
        self.calc_order_cost()     
        self.display_footer()
        
    def calc_order_cost(self):
        self.total_cost = 0.0 
        for part_key,part_i in self.parts.iteritems():
            self.total_cost += part_i.cost['material']*part_i.quantity
        
    def update_quantity(self):
        part_n = 1      
        del_keys = []
        for part_key,part_i in self.parts.iteritems():
            q_return = self.labels_part_quantities[part_key].get()
            print part_key,q_return
            try:
                part_i.quantity = int(q_return)                
                #self.warnings[part_key].config(text="                   ")
                self.warnings[part_key].config(text="")
            except:
                self.warnings[part_key].config(text="* non integer",fg="red")
                
            if( part_i.quantity  == 0 ):
                del_keys.append(part_key)
            part_n += 1
        # Delete zero quantity 
        for part_key in del_keys:
           del self.parts[part_key]
           del self.labels_part_names[part_key]
           del self.labels_part_quantities[part_key]
           del self.warnings[part_key]
           
        self.grid_parts()
        # Redisplay parts with updated quantities 
        part_n = 1
        for part_key,part_i in self.parts.iteritems():
            self.labels_part_quantities[part_key].delete(0,tk.END)
            self.labels_part_quantities[part_key].insert(0,part_i.quantity)
  
        
        self.calc_order_cost()     
        self.display_footer()
            
        
root = Tk()
#root.resizable(500,500)

my_gui = QuoteTool(root)
root.mainloop()