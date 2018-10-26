# parsing http://www.carmedia.co.kr/
# parsing http://server2.carmedia.co.kr/
# FOCUS (전체), NEWS (국산차, 수입차), REVIEW (시승기) 를 가져옴

# http://www.carmedia.co.kr/ 로 서버를 이전, 최신 데이터는 이곳에 있음
# http://server2.carmedia.co.kr/ 에 과거 몇 년 간의 데이터가 있음

import os
import sys
import pickle
import urllib.request
from bs4 import BeautifulSoup
from newspaper import Article

if __name__ == '__main__':

	# FOCUS 예전 사이트
	docURLs = list()
	docs = list()
	baseURL = 'http://server2.carmedia.co.kr/index.php?mid=focus&page={}'
	
	for idx in range(1, 2):
	#for idx in range(1, 566):

		page = urllib.request.urlopen(baseURL.format(idx))
		soup = BeautifulSoup(page, 'html')
		soup = soup.find('tbody').find_all('a', class_ = 'title')

		for t in soup:

			docURLs.append(t['href'])

	for docURL in docURLs:

		a = Article(docURL, language = 'ko')
		a.download()
		a.parse()

		print(a.title)
		print(a.date)
		print(a.text)



		"""
		page = urllib.request.urlopen(docURL)
		soup = BeautifulSoup(page, 'html')
		
		title = soup.find('a', class_ = 'title').text.strip()
		time = soup.find('span', class_ = 'date').text.strip()[6:16]
		mainText = ''

		soup = soup.find('div', class_ = 'boardReadBody').find('div')
		rows = soup.find('div').find_all('div')

		#print(len(rows), '\n')

		if len(rows) == 0:

			rows = soup.find_all('p')

		for row in rows:
			
			try:

				mainText = mainText + div.find('span').text

			except:

				pass
			

			mainText = mainText + row.getText()

		print(mainText)
		print('\n\n')

		"""

		docs.append({'title' : title, 'time' : time, 'content' : mainText})

	print(len(docs))

	with open('carMedia_old_focus.pickle', 'wb') as fs:

		pickle.dump(docs, fs)