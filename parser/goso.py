# parsing http://www.goso.co.kr

import os
import sys
import pickle
import urllib.request
from bs4 import BeautifulSoup

if __name__ == '__main__':

	# 소비자고발
	docURLs = list()
	docs = list()
	baseURL = 'http://www.goso.co.kr/bbs/board.php?bo_table=testDB&page={}'
	
	for idx in range(1, 2):
	#for idx in range(1, 8000 + 1):

		page = urllib.request.urlopen(baseURL.format(idx))
		soup = BeautifulSoup(page, 'lxml')
		soup = soup.find_all('td', class_ = 'subject')

		for t in soup[1:]:

			docURLs.append(t.find('a')['href'][2:])

	for docURL in docURLs:

		page = urllib.request.urlopen('http://www.goso.co.kr/' + docURL)
		soup = BeautifulSoup(page, 'lxml')
		
		#title = soup.find_all('table')[7].find('td').find('div').text.strip()
		time = '20' + soup.find('span').text[6:14]


		print(title, time)
		print('\n\n\n\n')
		
		"""
		soup = soup.find('div', id = 'articleBody').find_all('p')
		
		mainText = ''
		
		for p in soup:

			mainText = mainText + p.getText().replace('\n', '')

		docs.append({'title' : title, 'time' : time, 'content' : mainText})

	with open('goso.pickle', 'wb') as fs:

		pickle.dump(docs, fs)

		"""