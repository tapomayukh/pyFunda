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

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = '/home/tapo/git/personal_repos/client_secret.json'
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
        else: # Needed only for compatibility with Python 2.6
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

def main():
	"""Shows basic usage of the Gmail API.

	Creates a Gmail API service object and outputs a list of label names
	of the user's Gmail account.
	"""
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)

	results = service.users().labels().list(userId='me').execute()
	labels = results.get('labels', [])

	for label in labels:
		if label['name'] == 'Georgia Tech/Official Stuff/Gatech Related/From Prof':
			label_id = label['id']
	
	response = service.users().messages().list(userId='me',labelIds=label_id).execute()
	messages = []
	if 'messages' in response:
		messages.extend(response['messages'])

	while 'nextPageToken' in response:
		page_token = response['nextPageToken']
		response = service.users().messages().list(userId='me',labelIds=label_id,pageToken=page_token).execute()
		messages.extend(response['messages'])
	
	fwd_list_prof_email = []
	len_list_prof_email = []
	for msg in messages:
		message = service.users().messages().get(userId='me', id=msg['id']).execute()
		headers = message['payload']['headers']
		for header in headers:
			if header['name'] == 'Subject' and header['value'][0:3] == 'Fwd':
				fwd_list_prof_email.append(msg['id'])
			
	
	for msg in messages:
		if msg['id'] not in fwd_list_prof_email:
			relevant_message = service.users().messages().get(userId='me', id=msg['id']).execute()
			relevant_message_body = GetMessageBody(service,'me',msg['id'])
			print (relevant_message_body)			
			
if __name__ == '__main__':
	main()


