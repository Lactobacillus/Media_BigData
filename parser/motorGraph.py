# parsing http://www.motorgraph.com/
# 최신뉴스 (전체), 업계/정책 (완성차), 시승기/리뷰 (국산차, 수입차), 결함/문제점 (리콜), 커뮤니티 (자동차 정보/토론)

import os
import sys
import pickle
import urllib.request
from bs4 import BeautifulSoup

if __name__ == '__main__':

	# 최신뉴스 (전체) ==> [업계/정책 (완성차), 시승기/리뷰 (국산차, 수입차), 결함/문제점 (리콜)] 이 모두 포함
	docURLs = list()
	docs = list()
	baseURL = 'http://www.motorgraph.com/news/articleList.html?page={}'
	
	#for idx in range(1, 2):
	for idx in range(1, 700 + 1):

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
		soup = soup.find('div', id = 'articleBody').find_all('p')
		
		mainText = ''
		
		for p in soup:

			mainText = mainText + p.getText().replace('\n', '')

		docs.append({'title' : title, 'time' : time, 'content' : mainText})

	with open('motorgraph_news.pickle', 'wb') as fs:

		pickle.dump(docs, fs)

	# 커뮤니티 (자동차 정보/토론)
	docURLs = list()
	docs = list()
	baseURL = 'https://c.motorgraph.com/index.php?mid=info&page={}'
	
	#for idx in range(1, 2):
	for idx in range(1, 15 + 1):

		page = urllib.request.urlopen(baseURL.format(idx))
		soup = BeautifulSoup(page, 'lxml')
		soup = soup.find('table').find_all('a', class_ = 'hx')

		for t in soup:

			docURLs.append(t['href'])

	for docURL in docURLs:

		comments = list()

		page = urllib.request.urlopen(docURL)
		soup = BeautifulSoup(page, 'html')
		
		title = soup.find('h1', class_ = 'np_18px').text.split('            ')[1]
		time = soup.find('span', class_ = 'reg-date').text.strip()[0:10]
		mainText = soup.find('article', itemprop = 'articleBody').getText().replace('\n', ' ')

		soup = soup.find_all('div', id = 'cmtPosition')

		# 댓글이 있는 경우
		if len(soup) == 1:

			cmts = soup[0].find_all('li')

			for cmt in cmts:

				comments.append(cmt.find_all('div')[1].getText().strip().replace('\n', ' '))

		docs.append({'title' : title, 'time' : time, 'content' : mainText, 'reply' : comments})

	with open('motorgraph_board.pickle', 'wb') as fs:

		pickle.dump(docs, fs)