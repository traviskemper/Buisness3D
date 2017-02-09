# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 09:47:59 2017

@author: Travis Kemper
@email: travis.kemper.w@gmail.com

"""

import json

class Manufacture:
    def __init__(self,name):
        self.name = name 
        self.properties = {}
        
    def set_prop(self,set_prop):
        self.properties.update(set_prop)
        
    def write(self):
        with open('mf_{}.json'.format(self.name), 'w') as fp:
            json.dump(self.properties, fp,indent=4)
            
    def read(self):
        with open('mf_{}.json'.format(self.name)) as data_file:    
            self.properties = json.load(data_file)

    def validate(self):
        
        self.properties['target_income'] = max(self.properties['target_income'], 1)
        self.properties['operating_days'] = max(self.properties['operating_days'], 1)
        self.properties['operating_hours'] = max(self.properties['operating_hours'], 1)
        self.properties['discount_per_part'] = max(0, min(self.properties['discount_per_part'], 1) )
        self.properties['max_quantity_discount'] = min(self.properties['max_quantity_discount'], 1)
        self.properties['seconds_per_layer'] = max(self.properties['seconds_per_layer'], 0.001)
        self.properties['time_per_layer_leveling'] = max(self.properties['time_per_layer_leveling'], 0)
        self.properties['z_base_height'] = max(self.properties['z_base_height'], 0)
        
    def calc_prop(self):
        self.properties['cost_per_hour'] = self.properties['target_income'] / (self.properties['operating_days'] * self.properties['operating_hours'])
        
        