#!/usr/bin/env python

import sys
import imaplib
import getpass
import email
import datetime

def process_mailbox(M):
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return

        msg = email.message_from_string(data[0][1])
        print 'Message %s: %s' % (num, msg['Subject'])
        print 'Raw Date:', msg['Date']
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            print "Local Date:", local_date.strftime("%a, %d %b %Y %H:%M:%S")
        print 'Body Content:', msg.get_payload()

######################################################################################################

if __name__ == '__main__':

	M = imaplib.IMAP4_SSL('imap.gmail.com')
	try:
	    M.login('tapomayukh@gmail.com', getpass.getpass())
	except imaplib.IMAP4.error:
	    print "LOGIN FAILED!!! " # ... exit or deal with failure...

	rv, mailboxes = M.list()
	if rv == 'OK':
	    print "Mailboxes:"
        #print mailboxes

	rv, data = M.select("Georgia Tech/Internships/Disney")
	if rv == 'OK':
	    print "Processing mailbox...\n"
	    process_mailbox(M)
	    M.close()
	M.logout()






