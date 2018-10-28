# parsing http://www.autoview.co.kr/
# 뉴스 (전체), 구매가이드 (시승기, 리콜 정보)

import os
import sys
import pickle
import urllib.request
from bs4 import BeautifulSoup

if __name__ == '__main__':

	# 뉴스 (전체)
	docURLs = list()
	docs = list()
	baseURL = 'http://www.autoview.co.kr/content/news/news_total_list.asp?page={}'
	
	for idx in range(1, 2):
	#for idx in range(1, 2000 + 1):

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

		
		#soup = soup.find('div', class_ = 'article_text').find('div', class_ = 'article_text')
		



		#print(soup.getText().strip().replace('\n', ' '))
		#print('==========================================')




		#mainText = ''
		
		a = Article(docURL, language = 'ko')
		a.download()
		a.parse()

		print(a.text)
		print('========================')



		"""
		for p in soup:

			mainText = mainText + p.getText().replace('\n', '')

		docs.append({'title' : title, 'time' : time, 'content' : mainText})

	with open('autiview_news.pickle', 'wb') as fs:

		pickle.dump(docs, fs)
		"""