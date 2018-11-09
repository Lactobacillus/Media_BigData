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

		try:

			page = urllib.request.urlopen(baseURL.format(idx))
			soup = BeautifulSoup(page, 'lxml')
			soup = soup.find('div', class_ = 'article').find_all('li')

			for li in soup:

				docURLs.append(li.find('a')['href'])

		except:

			pass

	for docURL in docURLs:

		try:

			page = urllib.request.urlopen('http://www.autoview.co.kr' + docURL)
			soup = BeautifulSoup(page, 'lxml')
			
			title = soup.find('h4').text.strip()
			time = soup.find('div', class_ = 'article_info').getText().strip()[8:18]

			a = Article('http://www.autoview.co.kr' + docURL, language = 'ko')
			a.download()
			a.parse()

			mainText = a.text.strip().replace('\n', ' ')

			docs.append({'title' : title, 'time' : time, 'content' : mainText})

		except:

			pass

	with open('autiview_news.pickle', 'wb') as fs:

		pickle.dump(docs, fs)