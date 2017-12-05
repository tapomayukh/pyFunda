#!/usr/bin/env python

import urllib
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import time
import datetime
import sys
import schedule
import os, os.path

import numpy as np
import csv

apiKey = "Write your key here"
fileDirectory = "your path" # where to store the CSV file
filePrefix = "ProductivityData"

## Self explanatory function : Opens rescuetime data stored in a csv file, stores
## in a google spreadsheet (which creates the graph), and website embeds it

def save_data_to_google_spreadsheet(filePath):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('your json file', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open("grad_output").sheet1
    cell_list = wks.range('A1:B7')
    final_data = []
    new_row = []
    with open(filePath, 'rb') as csvfile:
	datareader = csv.reader(csvfile)
	i=1
	num_rows=0
	temp = 0.0
	for row in datareader:
	    num_rows=num_rows+1
            if row[0][0:4] != 'Date':
		year = int(float(row[0][0:4]))
		month = int(float(row[0][5:7]))
		day = int(float(row[0][8:10]))
		week_idx = datetime.datetime(year,month,day).weekday()
		if num_rows==2:
		    prev_week_idx = week_idx
		if prev_week_idx == 0:
		    week_day = 'Monday'
		elif prev_week_idx == 1:
		    week_day = 'Tuesday'
		elif prev_week_idx == 2:
		    week_day = 'Wednesday'
		elif prev_week_idx == 3:
		    week_day = 'Thursday'
		elif prev_week_idx == 4:
		    week_day = 'Friday'
		elif prev_week_idx == 5:
		    week_day = 'Saturday'
		elif prev_week_idx == 6:
		    week_day = 'Sunday'
		if row[-1] == '1' or '2':
		    temp = temp + float(row[1])
		if week_idx != prev_week_idx:
		    new_row = [week_day, np.str(temp/(14*3600.))]
		    final_data.append(new_row)
		    i=i+1
		    temp = 0.0
		    prev_week_idx = week_idx
		
	new_row = [week_day, np.str(temp/(14*3600.))]
	final_data.append(new_row)
	for i in range(len(cell_list)):
            print i
	    if i%2 == 0:
	        cell_list[i].value = final_data[i/2][0]
	    else:
	        cell_list[i].value = final_data[i/2][1]
	wks.update_cells(cell_list)
				

## Again pretty self-explanatory: Collects data in a 7-day format similar to 
## the Ph.D comic strip which I am trying to emulate here.. (refer www.tapomayukh.com)

## Collects data from rescuetime API and stores in a CSV file which 
## 'save_to_google_spreadsheet' function uses to upload in cloud

def run_algorithm():
    today = datetime.datetime.now()
    start_date = today + datetime.timedelta(days=-6)
    start_day = np.str(start_date.day)
    start_month = np.str(start_date.month)
    start_year = np.str(start_date.year)

    end_date = datetime.datetime.now()
    end_day = np.str(end_date.day)
    end_month = np.str(end_date.month)
    end_year = np.str(end_date.year)


    date_s = start_year+'-'+start_month+'-'+start_day
    date_e = end_year+'-'+end_month+'-'+end_day
    print "Getting Data for Interval", date_s, "to", date_e
    params = urllib.urlencode({'key':apiKey, 'perspective':'interval', 'format':'csv', 'restrict_begin':date_s, 'restrict_end':date_e, 'restrict_kind':'productivity', 'resolution_time':'day'})
    u = urllib.urlopen("https://www.rescuetime.com/anapi/data", params)
    CSVdata = u.read()
    filePath = fileDirectory + filePrefix + ".csv"
    f = open(filePath, "w")
    f.write(CSVdata)
    f.close()
    save_data_to_google_spreadsheet(filePath)

if __name__ == '__main__':

    # Runs at the end of day
    schedule.every().day.at("23:59").do(run_algorithm)

    while True:
    	schedule.run_pending()
	time.sleep(1)

