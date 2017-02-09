# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 09:42:37 2017


@author: Travis Kemper
@email: travis.kemper.w@gmail.com

"""

from manufacture import Manufacture

man = Manufacture('MountMfg')
man.read()
man.calc_prop()

print (man.properties)
