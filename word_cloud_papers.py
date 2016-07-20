#!/usr/bin/python

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

from wordcloud import WordCloud
import matplotlib.pyplot as pp

import os
import sys

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,password=password,caching=caching, check_extractable=True):

        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


if __name__ == '__main__':

	path_to_papers = '/home/tapo/my_papers/'
	file_name = path_to_papers + 'papers.txt'
	list_of_papers = os.listdir(path_to_papers)

	# Store all pdf files as text
	for paper in list_of_papers:
		with open(file_name, 'a+') as f:
			f.write(convert_pdf_to_txt(path_to_papers + paper))
			f.close()

	# Read the whole text file.
	text = open(file_name).read()

	# Generate a word cloud image
	wordcloud = WordCloud().generate(text)

	# Display the generated image:
	pp.imshow(wordcloud)
	pp.axis("off")

	# take relative word frequencies into account, lower max_font_size
	wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
	pp.figure()
	pp.imshow(wordcloud)
	pp.axis("off")
	pp.show()

	
	
