#!/usr/bin/python

import matplotlib
import numpy as np
import matplotlib.pyplot as pp
import math
import scipy as scp
import time
import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import sys
import schedule
import os, os.path

import csv

class Cnt_Lines:
	def __init__(self, paths):
		self.paths = paths
		today = datetime.datetime.now()
		self.day = today.day
		self.month = today.month
		self.year = today.year
		self.lines = 0

	def count_lines(self):
		for path_code in self.paths:
			for path,dirs,fs in os.walk(path_code):
				for f in fs:
					if f.lower().endswith('.py') or f.lower().endswith('.sh') or f.lower().endswith('.launch') or f.lower().endswith('.c') or f.lower().endswith('.cpp') or f.lower().endswith('.h') or f.lower().endswith('.m'):
						full_path  = path + '/' + f
						if os.path.isfile(full_path):
							with open(full_path) as f:
								self.lines = self.lines + sum(1 for _ in f if _.rstrip())

	def return_lines(self):
		return self.lines
	
	def return_date(self):
		return self.month, self.day, self.year

def run_algorithm(path_to_code):
	code = Cnt_Lines(path_to_code)
	code.count_lines()
	lines_today = code.return_lines()
	today_month, today_day, today_year = code.return_date()
	lines_data = [today_month, today_day, today_year, lines_today]
		
	save_data_to_google_spreadsheet(lines_data)

def save_data_to_google_spreadsheet(lines_data):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/tapo/git/project lines code-85f392792e73.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open("lines_of_code").sheet1
	
    data = wks.get_all_values()
    data_arr_prev = np.array(data)
    rows_prev, cols_prev = np.shape(data_arr_prev)
    if rows_prev <= 2:
        new_data = [str(lines_data[0])+'/'+str(lines_data[1])+'/'+str(lines_data[2]),str(0),str(lines_data[3])]
    else:
        prev_lines = data_arr_prev[2][cols_prev-1] 
        new_data = [str(lines_data[0])+'/'+str(lines_data[1])+'/'+str(lines_data[2]),str(float(lines_data[3])-float(prev_lines)), str(lines_data[3])]
    wks.insert_row(new_data,2)
	

if __name__ == '__main__':

    path_to_git_code1 = '/home/tapo/git/hrl-haptic-manip-dev/sandbox_tapo_darpa_m3/'
    path_to_git_code2 = '/home/tapo/git/projects_in_c_cpp/'
    path_to_git_code3 = '/home/tapo/git/projects_in_matlab/'
    path_to_git_code4 = '/home/tapo/git/projects_in_python/'
    path_to_git_code5 = '/home/tapo/git/pyFunda/'
    path_to_svn_robot1_code = '/home/tapo/svn/robot1/usr/tapo/'
    path_to_svn_robot1_data_code = '/home/tapo/svn/robot1_data/usr/tapo/data_code/'
    path_to_code = [path_to_git_code1, path_to_git_code2, path_to_git_code3, path_to_git_code4, path_to_git_code5, path_to_svn_robot1_code, path_to_svn_robot1_data_code]

    schedule.every().day.at("23:59").do(run_algorithm, path_to_code)

    while True:
        schedule.run_pending()
        time.sleep(1)
	
	
	
