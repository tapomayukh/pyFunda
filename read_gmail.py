#!/usr/bin/env python

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import base64
import email
from apiclient import errors

import nltk
from nltk.corpus import stopwords

import enchant

import matplotlib
import matplotlib.pyplot as pp

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'your json file path'
APPLICATION_NAME = 'Gmail API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def GetMessageBody(service, user_id, msg_id):
	try:
		local_message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
		msg_str = base64.urlsafe_b64decode(local_message['raw'].encode('ASCII'))
		mime_msg = email.message_from_string(msg_str)
		messageMainType = mime_msg.get_content_maintype()
		if messageMainType == 'multipart':
			for part in mime_msg.get_payload():
				if part.get_content_maintype() == 'text':
					return part.get_payload()
			return ""
		elif messageMainType == 'text':
			return mime_msg.get_payload()
	except errors.HttpError, error:
		print ('An error occurred: %s' % error)

def get_messages(user_id, label_name):
	
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)

	results = service.users().labels().list(userId=user_id).execute()
	labels = results.get('labels', [])

	for label in labels:
		if label['name'] == label_name:
			label_id = label['id']
	
	response = service.users().messages().list(userId=user_id,labelIds=label_id).execute()
	messages = []
	if 'messages' in response:
		messages.extend(response['messages'])

	while 'nextPageToken' in response:
		page_token = response['nextPageToken']
		response = service.users().messages().list(userId=user_id,labelIds=label_id,pageToken=page_token).execute()
		messages.extend(response['messages'])

	return service, messages

def post_process(text):
	# Post-processing using nltk
	tokens = nltk.wordpunct_tokenize(text)		
	tokens_alphabets = [w for w in tokens if w.isalpha()]
	return len(tokens_alphabets)
	

def from_prof(service, user_id, messages):	
	remove_list_prof_email = []
	len_list_prof_email = []
	for msg in messages:
		message = service.users().messages().get(userId=user_id, id=msg['id']).execute()
		headers = message['payload']['headers']
		for header in headers:
			if (header['name'] == 'Subject' and header['value'][0:3] == 'Fwd') or (header['name'] == 'From' and 'prof name' not in header['value']) or (header['name'] == 'To' and ',' in header['value']) or (header['name'] == 'To' and 'student name' not in header['value'] and 'Alt. student name' not in header['value']) or (header['name'] == 'Cc' and len(header['value']) > 0):
				remove_list_prof_email.append(msg['id'])
			
	for msg in messages:
		if msg['id'] not in remove_list_prof_email:
			relevant_message_body = GetMessageBody(service,'me',msg['id'])
			idx_list = [relevant_message_body.find('condition 1'), relevant_message_body.find('condition 2'), relevant_message_body.find('- ck'), relevant_message_body.find('>'), relevant_message_body.find('condition 3'), relevant_message_body.find('condition 4'), relevant_message_body.find('On')]
			idx_max = max(idx_list)
			if idx_max == -1:
				pass
			else:
				idx_min = min(x for x in idx_list if x > -1)	
				len_msg = post_process(relevant_message_body[:idx_min])
				len_list_prof_email.append(len_msg)
	return len_list_prof_email

def to_prof(service, user_id, messages):
	remove_list_my_email = []
	len_list_my_email = []
	for msg in messages:
		message = service.users().messages().get(userId=user_id, id=msg['id']).execute()
		headers = message['payload']['headers']
		for header in headers:
			if (header['name'] == 'Subject' and header['value'][0:3] == 'Fwd') or (header['name'] == 'From' and 'Student name' not in header['value'] and 'Alt student name' not in header['value']) or (header['name'] == 'To' and 'Prof name' not in header['value']) or (header['name'] == 'To' and ',' in header['value']) or (header['name'] == 'Cc' and len(header['value']) > 0):
				remove_list_my_email.append(msg['id'])

	for msg in messages:
		if msg['id'] not in remove_list_my_email:
			relevant_message_body = GetMessageBody(service,'me',msg['id'])
			idx_list = [relevant_message_body.find('Condition 1'), relevant_message_body.find('Condition 2'), relevant_message_body.find('>'), relevant_message_body.find('Condition 3'), relevant_message_body.find('Condition 4')]
			idx_max = max(idx_list)
			if idx_max == -1:
				pass
			else:
				idx_min = min(x for x in idx_list if x > -1)	
				len_msg = post_process(relevant_message_body[:idx_min])
				len_list_my_email.append(len_msg)
	return len_list_my_email

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d} ({p:.2f}%)'.format(p=pct,v=val)
    return my_autopct

def plot_data(prof_data, my_data):
	print (prof_data)
	print (my_data)
	matplotlib.rcParams['font.size'] = 16.0
	pie_labels = 'From Advisor', 'To Advisor'
	pie_nums = [prof_data, my_data]
	pie_colors = ['gold', 'lightskyblue']
	pie_explode = (0, 0.1)

	pp.pie(pie_nums, explode=pie_explode, labels=pie_labels, colors=pie_colors, autopct=make_autopct(pie_nums), shadow=True, startangle=90)
	pp.title('Average No. of Words per Email')
	pp.axis('equal')
				
			
if __name__ == '__main__':
	
	prof_label = 'Emails from Prof label'
	my_label = 'Emails to Prof label'
	
	service, prof_messages = get_messages('me',prof_label)
	prof_emails = from_prof(service, 'me', prof_messages)
	len_prof_emails = len(prof_emails)
	avg_words_prof = (float(sum(prof_emails))/float(len_prof_emails))

	service, my_messages = get_messages('me',my_label)
	my_emails = to_prof(service, 'me', my_messages)
	len_my_emails = len(my_emails)
	avg_words_me = (float(sum(my_emails))/float(len_my_emails))

	plot_data(avg_words_prof, avg_words_me)
	pp.show()


