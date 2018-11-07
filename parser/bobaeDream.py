# parsing http://www.bobaedream.co.kr/
# 국산차게시판, 수입차게시판, 자유게시판

import os
import sys
import pickle
import urllib.request
from bs4 import BeautifulSoup

if __name__ == '__main__':

	# 국산차게시판
	docURLs = list()
	docs = list()
	baseURL = 'http://www.bobaedream.co.kr/list?code=national&page={}'

	#for idx in range(1, 2):
	for idx in range(1, 25000 + 1):

		page = urllib.request.urlopen(baseURL.format(idx))
		soup = BeautifulSoup(page, 'lxml')
		soup = soup.find_all('tr', itemtype = 'http://schema.org/Article')

		for t in soup:

			docURLs.append(t.find('td', class_ = 'pl14').find('a')['href'])

	for docURL in docURLs:

		try:

			comments = list()

			page = urllib.request.urlopen('http://www.bobaedream.co.kr' + docURL)
			soup = BeautifulSoup(page, 'lxml')
			
			title = soup.find('div', class_ = 'writerProfile').find('strong').text.strip().split('[')[0]
			time = soup.find('div', class_ = 'writerProfile').find('span').find_all('em')[3]
			mainText = soup.find('div', class_ = 'bodyCont').text.strip().replace('\n', ' ').replace('\r', '')

			soup = soup.find('div', id = 'cmt_list')

			# 댓글
			if int(soup.find('span', class_ = 'comm2').text.replace('(', '').replace(')', '')) > 0:

				for li in soup.find('ul', id = 'cmt_reply').find_all('li'):

					comments.append(li.find('dd').text.strip())

			docs.append({'title' : title, 'time' : time, 'content' : mainText, 'reply' : comments})

		except:

			pass

	with open('bobaedream_board_national.pickle', 'wb') as fs:

		pickle.dump(docs, fs)

	# 수입차게시판
	docURLs = list()
	docs = list()
	baseURL = 'http://www.bobaedream.co.kr/list?code=import&page={}'

	#for idx in range(1, 2):
	for idx in range(1, 4000 + 1):

		page = urllib.request.urlopen(baseURL.format(idx))
		soup = BeautifulSoup(page, 'lxml')
		soup = soup.find_all('tr', itemtype = 'http://schema.org/Article')

		for t in soup:

			docURLs.append(t.find('td', class_ = 'pl14').find('a')['href'])

	for docURL in docURLs:

		try:

			comments = list()

			page = urllib.request.urlopen('http://www.bobaedream.co.kr' + docURL)
			soup = BeautifulSoup(page, 'lxml')
			
			title = soup.find('div', class_ = 'writerProfile').find('strong').text.strip().split('[')[0]
			time = soup.find('div', class_ = 'writerProfile').find('span').find_all('em')[3]
			mainText = soup.find('div', class_ = 'bodyCont').text.strip().replace('\n', ' ').replace('\r', '')

			soup = soup.find('div', id = 'cmt_list')

			# 댓글
			if int(soup.find('span', class_ = 'comm2').text.replace('(', '').replace(')', '')) > 0:

				for li in soup.find('ul', id = 'cmt_reply').find_all('li'):

					comments.append(li.find('dd').text.strip())

			docs.append({'title' : title, 'time' : time, 'content' : mainText, 'reply' : comments})

		except:

			pass

	with open('bobaedream_board_import.pickle', 'wb') as fs:

		pickle.dump(docs, fs)