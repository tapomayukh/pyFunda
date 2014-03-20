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
import unittest

class Problem:
    def __init__(self, level_num, input_str):
        self.level_num = level_num
        self.input_str = input_str
         
    def apply_rule(self, param):
        # Params
        look_ahead = param
        
        # Body
        intab = string.ascii_lowercase
        intab_len = len(intab)
        outtab = ''
        for i in range(intab_len-look_ahead):
            outtab = outtab + chr(ord(intab[i])+look_ahead)
        for i in range(look_ahead):
            outtab = outtab + chr(ord(intab[i]))
                
        trantab = string.maketrans(intab, outtab)
        result = self.input_str.translate(trantab)
        return result
            
    def gen_output(self, param):
        output = self.apply_rule(param)  
        return output
        
    
######################################################################################################

if __name__ == '__main__':
    
    inp_string = raw_input("Enter a string to be converted:")
    level_no = 1
    letters_look_ahead = 2
    
    level_1 = Problem(level_no, inp_string)
    solution = level_1.gen_output(letters_look_ahead)
    
    print "The solution to Level ", level_no, " is: "
    print solution
        
    
    
    
        

    
    
   

    
    

    
    
    
        

    
    
   

    
    
