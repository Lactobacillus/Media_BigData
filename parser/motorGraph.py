# parsing http://www.motorgraph.com/
# 최신뉴스 (전체), 업계/정책 (완성차), 시승기/리뷰 (국산차, 수입차), 결함/문제점 (리콜), 커뮤니티 (자동차 정보/토론)

import os
import sys
import pickle
import urllib.request
from bs4 import BeautifulSoup
#from newspaper import Article

if __name__ == '__main__':

	# 최신뉴스 (전체) 에 {업계/정책 (완성차), 시승기/리뷰 (국산차, 수입차), 결함/문제점 (리콜)} 이 모두 포함
	docURLs = list()
	docs = list()
	baseURL = 'http://www.motorgraph.com/news/articleList.html?page={}'
	
	for idx in range(1, 2):
	#for idx in range(1, 700):

		page = urllib.request.urlopen(baseURL.format(idx))
		soup = BeautifulSoup(page, 'lxml')
		soup = soup.find('section', class_ = 'article-list-content').find_all('a', class_ = 'links')

		for t in soup:

			docURLs.append(t['href'])

	for docURL in docURLs:

		page = urllib.request.urlopen('http://www.motorgraph.com' + docURL)
		soup = BeautifulSoup(page, 'html')
		
		title = soup.find('div', class_ = 'article-head-title').text.strip()
		time = soup.find('div', class_ = 'info-text').find_all('li')[2].text.strip()[3:13]
		
		mainText = ''

		soup = soup.find('div', id = 'articleBody').find_all('p')
		
		for p in soup:

			mainText = mainText + p.getText().replace('\n', '')

		docs.append({'title' : title, 'time' : time, 'content' : mainText})

	with open('motorgraph_news.pickle', 'wb') as fs:

		pickle.dump(docs, fs)
		