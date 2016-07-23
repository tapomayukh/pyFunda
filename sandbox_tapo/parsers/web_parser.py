#!/usr/bin/env python

import twill.commands as com
from bs4 import BeautifulSoup
import urllib2

from xlrd import open_workbook
from xlwt import *
#from openpyxl import load_workbook
from xlutils.copy import copy

import numpy as np
import scipy as scp
import unicodedata
import time
from string import maketrans

def find_price(name, vintage, volume):

	formlist = []
	#com.showforms()
	all_forms = cbrw.get_all_forms()
	for each_form in all_forms:
		formlist.append(each_form.name)
	if 'searchform' in formlist:
		com.formclear("searchform")
		com.fv("searchform", "Xwinename", name)
		com.fv("searchform", "Xvintage", vintage)
		com.fv("searchform", "Xstateid", "CA")
		com.fv("searchform", "Xbottle_size", "Bottles")
		#com.fv("searchform", "Xprice_set", "CUR")
		com.submit()    
		url = com.browser.get_url()
		#print url

		page=urllib2.urlopen(url)

		soup = BeautifulSoup(page.read())
		prices=soup.findAll('span',{'class':'offer_price boldtxt'})

		price_values = []
		for price in prices:
			#print float((price.next).replace(",", ""))
			price_values.append(float((price.next).replace(",", "")))

		if len(price_values) > 0:
			return min(price_values), max(price_values), np.mean(price_values)
		else:
			return 'unknown', 'unknown', 'unknown'
	else:
		return 'unknown', 'unknown', 'unknown'

######################################################################################################

if __name__ == '__main__':

	min_price_list = []
	max_price_list = []
	avg_price_list = []
	delay_time = 1

	cbrw = com.get_browser()
	cbrw.go('your website')

	com.showforms()
	com.fv("loginform", "login_id_F", "your id")
	com.fv("loginform", "password_F", "your passwd")
	com.submit()
	
### Access Excel Entries ####

	wb = open_workbook('filename.xls')
	for sheet in wb.sheets():
	   	if sheet.number == 0:
			item_names = sheet.col_values(5, start_rowx=1)
			bottle_volumes = sheet.col_values(9, start_rowx=1)
			vintages = sheet.col_values(13, start_rowx=1)
			
	data_len = len(item_names)
	intab = "a"
	outtab = "a"
	trantab = maketrans(intab, outtab)
	for i in range(data_len):
		item_names[i] = unicodedata.normalize('NFKD', item_names[i]).encode('ascii','ignore')
		item_names[i] = item_names[i].translate(trantab,'0123456789')
		if item_names[i][-2:] == 'yr':
			item_names[i] = item_names[i][:-2]
		if item_names[i][-4:] == 'year':
			item_names[i] = item_names[i][:-4]
		item_names[i] = item_names[i][0:item_names[i].find("(")]+item_names[i][item_names[i].find(")")+1:]
		item_names[i] = item_names[i].strip()
		print 'Searching Item Number : ', i+1, ' out of ', data_len, ' items in Excel Sheet'
		print 'Item name : ', item_names[i], ' Vintage : ', str(int(vintages[i]))
		min_p, max_p, avg_p = find_price(item_names[i], str(int(vintages[i])), bottle_volumes[i])
		min_price_list.append(min_p)
		max_price_list.append(max_p)
		avg_price_list.append(avg_p)
		if i > 45*delay_time:
			time.sleep(600) # delays for 10 minutes
			delay_time = delay_time + 1
	cbrw.go('your logout id')

	#print min_price_list, max_price_list, avg_price_list

	wb_modified = copy(wb)
	sh_modified = wb_modified.get_sheet(0)
	for i in range(data_len):
		sh_modified.write(i+1, 17, min_price_list[i])
		sh_modified.write(i+1, 18, max_price_list[i])
		sh_modified.write(i+1, 19, avg_price_list[i])
	wb_modified.save('filename.xls')
	
	
			
		        
    
    










