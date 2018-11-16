# parsing http://www.bobaedream.co.kr/
# 국산차게시판, 수입차게시판, 자유게시판

import os
import sys
import pickle
import asyncio
import itertools
import multiprocessing
from time import sleep
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
from aiohttp import ClientSession as cs

async def getOnePage(url):

	async with cs() as sess:

		async with sess.get(url) as resp:

			return await resp.text()

def parseURL(html):

	docURLs = list()

	soup = BeautifulSoup(html, 'lxml')
	soup = soup.find_all('tr', itemtype = 'http://schema.org/Article')

	for t in soup:

		docURLs.append(t.find('td', class_ = 'pl14').find('a')['href'])

	return docURLs

def parseArticle(html):

	docs = list()



if __name__ == '__main__':

	# 국산차게시판
	docURLs = list()
	docHTMLs = list()
	docs = list()
	task = list()
	baseURL = 'http://www.bobaedream.co.kr/list?code=national&page={}'

	loop = asyncio.get_event_loop()
	
	for idx in range(1, 10):
	#for idx in range(1, 25000 + 1):

		task.append(asyncio.ensure_future(getOnePage(baseURL.format(idx))))

		if idx % 100 == 0:

			loop.run_until_complete(asyncio.wait(task))
			sleep(2)

	loop.close()

	docURLs = list(itertools.chain.from_iterable(Parallel(
		n_jobs = multiprocessing.cpu_count())(delayed(parseURL)(page) for page in [t.result() for t in task])))



"""

	for docURL in docURLs:

		try:

			comments = list()

			page = urllib.request.urlopen('http://www.bobaedream.co.kr' + docURL)
			soup = BeautifulSoup(page, 'lxml')
			
			title = soup.find('div', class_ = 'writerProfile').find('strong').text.strip().split('[')[0]
			time = soup.find('span', class_ = 'countGroup').text[-20:-10]
			mainText = soup.find('div', class_ = 'bodyCont').text.strip().replace('\n', ' ').replace('\r', '')

			soup = soup.find('div', id = 'cmt_list')

			# 댓글
			if int(soup.find('span', class_ = 'comm2').text.replace('(', '').replace(')', '')) > 0:

				for li in soup.find('ul', id = 'cmt_reply').find_all('li'):

					comments.append(li.find('dd').text.strip())

			docs.append({'title' : title, 'time' : time, 'content' : mainText, 'reply' : comments})

		except:

			pass




	with open('bobaedream_board_national.txt', 'w') as fs:

		fs.write(str(docs))
"""