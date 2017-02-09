# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 10:08:28 2017

@author: Travis Kemper
@email: travis.kemper.w@gmail.com

"""

import numpy
from stl import mesh
import datetime

class Order:
    def __init__(self):
        self.date = datetime.datetime.now()
        self.parts = {}
        self.number = 0
        self.df = None
        
class Material:
    
    def __init__(self,name):
        self.name = name 
        self.density = 0.001 #g/mm^3 
        self.cost_g = 100.0
        
class Part:
    def __init__(self,name):
        
        self.name = name 
        self.mesh = None 
        self.properties = {}
        self.units = 'mm'        
        self.qty = 1
        self.materials = {}
        self.notes = ""
        self.auto_orient = True
        self.cost = 0.0 
        
        
    def read_mesh(self,stl_file):
        self.stl_file = stl_file
        self.mesh = mesh.Mesh.from_file(stl_file)
        
    def calc_props(self):
                
        volume, cog, inertia = self.mesh.get_mass_properties()
        self.properties['Volume'] = volume
        
        
        mesh_size = self.mesh.max_ -  self.mesh.min_
        
        self.properties['Size'] = mesh_size
        
        surf_areas = numpy.zeros(3)
        surf_areas[0] =  mesh_size[0]* mesh_size[1] # XY
        surf_areas[1] =  mesh_size[1]* mesh_size[2] # YZ
        surf_areas[2] =  mesh_size[2]* mesh_size[0] # XZ
        self.properties['SrufAreas'] = surf_areas #[ round(s,3) for s in surf_areas] 
        
        # Find surface area and height based on given orientation 
        self.properties['SrufArea'] = surf_areas[0]
        self.properties['Height'] =  mesh_size[2]
        
        if( self.auto_orient ):
            max_area_index = numpy.argmax(surf_areas)
            self.properties['SrufArea'] = surf_areas[max_area_index] 
            
            if( max_area_index == 0 ):
                #area_id = 'XY'
                self.properties['Height'] = mesh_size[2]
                self.properties
            elif( max_area_index == 1 ):
                #area_id = 'YZ'
                self.properties['Height'] = mesh_size[0]
            elif( max_area_index == 2 ):
                #area_id = 'XZ'
                self.properties['Height'] = mesh_size[1]
                
        