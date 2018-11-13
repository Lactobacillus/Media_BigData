import sys
import pickle
from datetime import datetime

if __name__ == '__main__':

	dataList = list()

	for arg in sys.argv[1:]:

		with open(arg, 'rb') as fs:

			data = pickle.load(fs)

		for d in data:

			try:

				d['time'] = d['time'].replace('-', '.')
				d['time'] = datetime.strptime(d['time'], '%Y.%m.%d')

			except:

				pass

			else:

				dataList.append(d)

	print('# of total data : ', len(dataList))

	with open('integrated_data.pickle', 'wb') as fs:

		pickle.dump(dataList, fs)