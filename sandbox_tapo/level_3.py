#!/usr/bin/env python

# Level 1

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
import re
import unittest

class Problem:
    def __init__(self, level_num, input_str):
        self.level_num = level_num
        self.input_str = input_str
         
    def apply_rule(self, param):
        # Params
        ltr_fwd_back = param

        # Body
        pattern = r"\b[A-Z]{3}[a-z][A-Z]{3}\b"
        d = re.match(pattern, self.input_str)
        return d.group(0)
            
    def gen_output(self, param):
        output = self.apply_rule(param)  
        return output
        
    
######################################################################################################

if __name__ == '__main__':

    
    filename = "equality.txt"
    sub_dir = "./data/"
    f = open(os.path.join(sub_dir, filename))
    inp_string = f.read()
    
    level_no = 3
    fwd_back = 3
        
    level = Problem(level_no, inp_string)
    solution = level.gen_output(fwd_back)        
        
    print "The solution to Level ", level_no, " is:", solution
        
