import sys
import os
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize
import nltk
import xml.etree.ElementTree as ET
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
import sklearn.feature_extraction.text as texter
from itertools import islice
import numpy as np
from sklearn import decomposition

graph = {}
dataset = []
i=0
with open('index.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		if i==0:
			i=1
		else:
			if row[1] in graph.keys() and not row[0] in graph[row[1]]:
				graph[row[1]].append(row[0])
			else:
				graph[row[1]] = [row[0],]

#print (graph[0])
'''
for row in graph.keys():
	str = join("data/",row) + "/" + row + "_1.txt"
	print (str)
	dataset.append(str);
	for citations in graph[row]:
		print (citations)
		str = join("data/",row) + "/" + row + "_1.txt"
		dataset.append(str)
	vectorizer = texter.CountVectorizer(input='filename', stop_words='english', min_df=1)
	dtm = vectorizer.fit_transform(dataset).toarray()
	vocab = np.array(vectorizer.get_feature_names())
	print (dtm.shape)
	print (len(vocab))
	#print (dataset)
	sys.exit()
	'''
files = []
directories =[join("data/",d) for d in listdir("data/")]

for d in directories:
	st = [join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-6:]=="_1.txt"]
	files.append([join(d,f) for f in listdir(d) if isfile(join(d, f)) and f[-6:]=="_1.txt"])
	dataset.append(str(st)[2:-2])

print (len(files))
#print (files[0])
print (len(dataset))
print (dataset[0])
#map(dataset,files)
#print (dataset[0])

vectorizer = texter.CountVectorizer(input='filename', stop_words='english', min_df=20)
dtm = vectorizer.fit_transform(dataset).toarray()
vocab = np.array(vectorizer.get_feature_names())
print (dtm.shape)
print (len(vocab))
num_topics = 20
num_top_words = 20
clf = decomposition.NMF(n_components=num_topics, random_state=1)
doctopic = clf.fit_transform(dtm)
topic_words = []
for topic in clf.components_:
	word_idx = np.argsort(topic)[::-1][0:num_top_words]
	topic_words.append([vocab[i] for i in word_idx])
doctopic = doctopic / np.sum(doctopic, axis=1, keepdims=True)
print (doctopic[0].sum())
print (doctopic[0][0])
print (doctopic.shape)
result = np.array(doctopic)
print (result.shape)
print (result[0][0])


temp = []


i=0
#with open('eggs.csv', 'wb') as csvfile:
#    spamwriter = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
with open('index.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		if i==0:
			i=1
		else:
			paper1 = join("data/",row[0]) + "/" + row[0] + "_1.txt"
			paper2 = join("data/",row[1]) + "/" + row[1] + "_1.txt"
			print (paper1)
			print (paper2)
			for idx, paper in enumerate(dataset):
				if paper == paper1:
					idx1 = idx
				if paper == paper2:
					idx2 = idx
			temp.append(np.dot(result[idx1],result[idx2]))
			#sys.exit()

res_to_write = np.array(temp)
np.savetxt("feature_k12.csv", res_to_write, delimiter=",")
'''
novel_names = []
for fn in dataset:
	basename = os.path.basename(fn)
	name, ext = os.path.splitext(basename)
	name = name.rstrip('0123456789')
	novel_names.append(name)
novel_names = np.asarray(novel_names)
doctopic_orig = doctopic.copy()
num_groups = len(set(novel_names))
doctopic_grouped = np.zeros((num_groups, num_topics))
for i, name in enumerate(sorted(set(novel_names))):
	doctopic_grouped[i, :] = np.mean(doctopic[novel_names == name, :], axis=0)
doctopic = doctopic_grouped
print (doctopic[0].sum())
print (doctopic[0][0])
'''
sys.exit()