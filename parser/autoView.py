# parsing http://www.autoview.co.kr/
# 뉴스 (전체), 구매가이드 (시승기, 리콜 정보, 차량구입 Q&A)

import os
import sys
import pickle
import urllib.request
from bs4 import BeautifulSoup
from newspaper import Article

if __name__ == '__main__':

	# 뉴스 (전체)
	docURLs = list()
	docs = list()
	baseURL = 'http://www.autoview.co.kr/content/news/news_total_list.asp?page={}'
	
	#for idx in range(1, 2):
	for idx in range(1, 2000 + 1):

		page = urllib.request.urlopen(baseURL.format(idx))
		soup = BeautifulSoup(page, 'lxml')
		soup = soup.find('div', class_ = 'article').find_all('li')

		for li in soup:

			docURLs.append(li.find('a')['href'])

	for docURL in docURLs:

		page = urllib.request.urlopen('http://www.autoview.co.kr' + docURL)
		soup = BeautifulSoup(page, 'html')
		
		title = soup.find('h4').text.strip()
		time = soup.find('div', class_ = 'article_info').getText().strip()[8:18]

		a = Article('http://www.autoview.co.kr' + docURL, language = 'ko')
		a.download()
		a.parse()

		mainText = a.text.strip().replace('\n', ' ')

		docs.append({'title' : title, 'time' : time, 'content' : mainText})

	with open('autiview_news.pickle', 'wb') as fs:

		pickle.dump(docs, fs)

	"""

	# 구매가이드 (시승기)
	docURLs = list()
	docs = list()
	baseURL = 'http://www.autoview.co.kr/content/buyer_guide/guide_road.asp?page={}'
	
	for idx in range(1, 2):
	#for idx in range(1, 2000 + 1):

		page = urllib.request.urlopen(baseURL.format(idx))
		soup = BeautifulSoup(page, 'lxml')
		soup = soup.find('div', class_ = 'article').find_all('li')

		for li in soup:

			docURLs.append(li.find('a')['href'])










	with open('autiview_guide.pickle', 'wb') as fs:

		pickle.dump(docs, fs)

	# 구매가이드 (리콜 정보)
	docURLs = list()
	docs = list()
	baseURL = 'http://www.autoview.co.kr/content/buyer_guide/recall_news.asp?page={}'









	with open('autiview_recall.pickle', 'wb') as fs:

		pickle.dump(docs, fs)

	# 구매가이드 (차량구입 Q&A) => 해야 하나?
	docURLs = list()
	docs = list()
	baseURL = 'http://www.autoview.co.kr/bbs/board.asp?page={}&news_section=qna'
	








	with open('autiview_qna.pickle', 'wb') as fs:

		pickle.dump(docs, fs)
	"""