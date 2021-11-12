# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 16:33:51 2021

@author: LIKITH
"""

import os 
import shutil

for x in os.listdir(r'E:\MTP2\data\SMOS data raw\RE04\MIR_CLF31A\2015'):
    folder= os.path.join(r'E:\MTP2\data\SMOS data raw\RE04\MIR_CLF31A\2015',x)
    if os.path.isdir(folder):
        for y in os.listdir(folder):
            shutil.move(os.path.join(folder, y),r'E:\MTP2\data\SMOS data raw\RE04\MIR_CLF31A\2015')
        os.rmdir(folder)