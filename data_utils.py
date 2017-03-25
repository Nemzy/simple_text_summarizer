# |----------------------------------------|
# |Creates a dataset from raw text files   |
# |----------------------------------------|
# |Dataset: BBCSport                       |
# |URL: http://mlg.ucd.ie/datasets/bbc.html| 
# |Creator: Nemanja Tomic                  |
# |----------------------------------------|

import cPickle as pickle
import os
from collections import Counter

titles = []
contents = []

def get_data_from_article(file_path):

	with open(file_path, 'r') as article:

		lines = article.read().split('\n')

		titles.append(lines[0])

		content = ''
		for i in range(1, len(lines)):
			if lines[i] == '':
				continue
			content += lines[i] + ' '

		contents.append(content)

def make_data_set(drop_n = 0):
	vocab_dict = Counter(w.strip(',."\' ;:)(?!') for txt in titles+contents for w in txt.split())
	vocab = map(lambda x: x[0], sorted(vocab_dict.items(), key = lambda x: -x[1]))

	if drop_n > 0:
		vocab = vocab[:-drop_n]

	word2idx = dict([(word, idx+2) for idx, word in enumerate(vocab)])
	word2idx['<ukn>'] = 0
	word2idx['<eos>'] = 1

	idx2word = dict([(idx, word) for word, idx in word2idx.iteritems()])

	Y = [[word2idx.get(word.strip(',."\' ;:)(?!'), 0) for word in title.split()] for title in titles]
	X = [[word2idx.get(word.strip(',."\' ;:)(?!'), 0) for word in content.split()] for content in contents]

	return X, Y, word2idx, idx2word, vocab

def save_data_set(filename, obj):
	with open(filename, 'wb') as f:
		pickle.dump(obj, f, -1)

def read_data_set(filename):
	with open(filename, 'rb') as f:
		return pickle.load(f)


if __name__ == '__main__':

	walk = os.walk('../data/')
	next(walk)
	for dirpath, dirnames, filenames in walk:
		for filename in filenames:
			get_data_from_article(os.path.join(dirpath, filename))
	save_data_set(filename = 'data.pkl', obj = make_data_set())