#!/usr/bin/python

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as pp
from PIL import Image
import os
from os import path
import sys
import numpy as np
import nltk
from nltk.corpus import stopwords

import enchant

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

	path_to_papers_before_phd = '/home/tapo/my_papers/before_phd/'
	path_to_papers_during_phd = '/home/tapo/my_papers/during_phd/'
        path_to_papers_after_phd = '/home/tapo/my_papers/after_phd/'
	path_to_images = '/home/tapo/my_papers/images/'

	names_list = ['before','during','after']
	idx = 0
	for path_to_papers in [path_to_papers_before_phd, path_to_papers_during_phd, path_to_papers_after_phd]:
		file_name = path_to_papers + 'papers.txt'

		# Delete the text file if it exists
		if os.path.exists(file_name):
			os.remove(file_name)
	
		list_of_papers = os.listdir(path_to_papers)
		
		# Store all pdf files as text
		for paper in list_of_papers:
			with open(file_name, 'a+') as f:
				f.write(convert_pdf_to_txt(path_to_papers + paper))
				f.close()

		# Read the whole text file.
		text = open(file_name).read().lower()

		# Post-processing using nltk
		tokens = nltk.wordpunct_tokenize(text)		
		tokens_alphabets = [w for w in tokens if w.isalpha()]
		tokens_cleaned = [w for w in tokens_alphabets if (len(w) > 2 and len(w) < 12)]
		modifiedStopWords = set(stopwords.words("english"))
		#add custom words
		modifiedStopWords.update(('vol','fig','cation','used','using','based','also'))
		filtered_words = [word for word in tokens_cleaned if word not in modifiedStopWords]

		# Spell Check using pyenchant
		d = enchant.Dict("en_US")
		final_words = [word for word in filtered_words if d.check(word)]		

		text = " ".join(final_words)
		
		# Generate a word cloud image
		robot_mask = np.array(Image.open(path.join(path_to_images, "robot.png")))
		# by taking relative word frequencies into account, lower max_font_size
		wc = WordCloud(background_color="white", max_words=2000, mask=robot_mask, contour_width=1, contour_color='white', max_font_size=40, relative_scaling=.5).generate(text)

                # store to file
		wc.to_file(path.join(path_to_images, names_list[idx]+".png"))

		# create coloring from image
		image_colors = ImageColorGenerator(robot_mask)

		# Generate a wordcloud image in the mask color
		wc.recolor(color_func=image_colors)

		# store to file
		wc.to_file(path.join(path_to_images, names_list[idx]+"2.png"))
                
		# Display the generated image:
		#pp.imshow(wc, interpolation='bilinear')
		#pp.axis("off")
		#pp.show()

		idx=idx+1

	
	
