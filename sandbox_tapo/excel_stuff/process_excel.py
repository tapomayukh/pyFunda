#!/usr/bin/env python

from xlrd import open_workbook
from xlwt import *
#from openpyxl import load_workbook
from xlutils.copy import copy

import numpy as np
import scipy as scp
import unicodedata
from string import *

from collections import OrderedDict

######################################################################################################

if __name__ == '__main__':

	wb = open_workbook('filename.xls')
	for sheet in wb.sheets():
		if sheet.number == 0:
			item_names_ref = sheet.col_values(1, start_rowx=1)
	   	if sheet.number == 1:
			item_names = sheet.col_values(5, start_rowx=1)
						
	data_len_ref = len(item_names_ref)
	for i in range(data_len_ref):
		item_names_ref[i] = unicodedata.normalize('NFKD', item_names_ref[i]).encode('ascii','ignore').lower()
		
	# Delete Duplicate Entries
	item_names = list(OrderedDict.fromkeys(item_names))

	data_len = len(item_names)
	intab = "a"
	outtab = "a"
	trantab = maketrans(intab, outtab)
	for i in range(data_len):
		item_names[i] = (item_names[i]).lower()
		item_names[i] = item_names[i].replace('\n','')
		item_names[i] = unicodedata.normalize('NFKD', item_names[i]).encode('ascii','ignore')
		item_names[i] = item_names[i].translate(trantab,'0123456789')
		if item_names[i][-2:] == 'yr':
			item_names[i] = item_names[i][:-2]
		if item_names[i][-4:] == 'year':
			item_names[i] = item_names[i][:-4]
		item_names[i] = item_names[i].strip()
	
	#print item_names_ref
	#print item_names
	#print len(item_names)

	j = 0
	idxs = np.zeros((len(item_names),1))
	item_number_list = [[] for i in range(len(item_names))]
	original_item_name_list = [[] for i in range(len(item_names))]
	for item_name in item_names:
		for item_name_ref in item_names_ref:
			if item_name in item_name_ref: 
				#print item_name_ref, item_names_ref.index(item_name_ref)+1
				idxs[j] = 1
				item_number_list[j].append(item_names_ref.index(item_name_ref)+1)
				original_item_name_list[j].append(item_name_ref)
		j = j+1

	#print idxs

	j = 0
	for item_name in item_names:
		if idxs[item_names.index(item_name)] == 0 and len(item_name.split()) > 2:
			item_name_3_words = ' '.join([item_name.split()[0],item_name.split()[1],item_name.split()[2]])
			for item_name_ref in item_names_ref:
				if item_name_3_words in item_name_ref: 
					#print item_name_ref, item_names_ref.index(item_name_ref)+1
					idxs[j] = 1
					item_number_list[j].append(item_names_ref.index(item_name_ref)+1)
					original_item_name_list[j].append(item_name_ref)
		j = j+1

	#print idxs

	j = 0
	for item_name in item_names:
		if idxs[item_names.index(item_name)] == 0 and len(item_name.split()) > 1:
			item_name_2_words = ' '.join([item_name.split()[0],item_name.split()[1]])
			for item_name_ref in item_names_ref:
				if item_name_2_words in item_name_ref: 
					#print item_name_ref, item_names_ref.index(item_name_ref)+1
					idxs[j] = 1
					item_number_list[j].append(item_names_ref.index(item_name_ref)+1)
					original_item_name_list[j].append(item_name_ref)
		j = j+1

	#print idxs
		
	j = 0
	for item_name in item_names:
		if idxs[item_names.index(item_name)] == 0 and len(item_name.split()) > 1:
			item_name_1_word_1_letter = ' '.join([item_name.split()[0],item_name.split()[1][0]])
			for item_name_ref in item_names_ref:
				if item_name_1_word_1_letter in item_name_ref: 
					#print item_name_ref, item_names_ref.index(item_name_ref)+1
					idxs[j] = 1
					item_number_list[j].append(item_names_ref.index(item_name_ref)+1)
					original_item_name_list[j].append(item_name_ref)
		j = j+1

	#print idxs
	#print item_number_list
	#print original_item_name_list
	for i in np.where(idxs == 0)[0]:
		print item_names[i] 	

	wb_modified = copy(wb)
	sh_modified = wb_modified.get_sheet(1)
	for i in range(len(item_names)):
		sh_modified.write(i+1, 6, str(item_number_list[i]))
		sh_modified.write(i+1, 7, str(original_item_name_list[i]))
	wb_modified.save('filename.xls')
	
			
		        
    
    










