# parsing http://www.bobaedream.co.kr/
# 국산차게시판, 수입차게시판, 자유게시판

import os
import sys
import pickle
import asyncio
import multiprocessing
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

if __name__ == '__main__':

	loop = asyncio.get_event_loop()

	baseURL = 'http://www.bobaedream.co.kr/list?code=national&page={}'

	docURLs = list()
	docs = list()
	task = list()

	for idx in range(1, 10):
	#for idx in range(1, 25000 + 1):

		task.append(asyncio.ensure_future(getOnePage(baseURL.format(idx))))


	loop.run_until_complete(asyncio.wait(task))


	result = [t.result() for t in task]

	ll = Parallel(n_jobs = multiprocessing.cpu_count())(delayed(parseURL)(page) for page in result)

	for l in ll:

		docURLs = docURLs + l

	print(docURLs)