#!/usr/bin/env python

# Level 2

import pylab as pyl
import numpy as np
import matplotlib.pyplot as pp
import scipy as scp
import scipy.ndimage as ni

import copy
import pickle
import optparse
import string
from collections import Counter
import os
import unittest

class Problem:
    def __init__(self, level_num, input_str):
        self.level_num = level_num
        self.input_str = input_str
         
    def apply_rule(self):
        # Params
        d = {}

        # Body
        for letter in self.input_str:
            d[letter] = self.input_str.count(letter)
        
        return d
            
    def gen_output(self):
        output = self.apply_rule()
        
        #for k in sorted(output):
            #print (k + ': ' + str(solution[k]))
            
        output_str = "".join(ch for ch in self.input_str if output[ch] == 1)  
        return output_str
        
    
######################################################################################################

if __name__ == '__main__':

    
    filename = "ocr.txt"
    sub_dir = "./data/"
    f = open(os.path.join(sub_dir, filename))
    inp_string = f.read()
    
    level_no = 2
        
    level = Problem(level_no, inp_string)
    solution = level.gen_output()        
        
    print "The solution to Level ", level_no, " is:", solution
        
