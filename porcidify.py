import argparse
import json
import numpy
import re
import sklearn.cluster
import sys

parser = argparse.ArgumentParser(description='make porcids from pubs')
parser.add_argument('json', help='publications in json')
parser.add_argument('--verbose', action='store_true', help='show progress')
arg = parser.parse_args()

def distance(P, Q):
	shared = 0
	for p in P:
		if p in Q: shared += 1
	return 1 - shared * 2 / ( len(P) + len(Q) )

## Read publication data
with open(arg.json) as fp:
	data = json.load(fp)

# represent as 2d np array
npd = numpy.zeros(shape=(len(data), len(data)))
for i in range(len(data)):
	for j in range(len(data)):
		names1 = [x['name'] for x in data[i]['authors']]
		names2 = [x['name'] for x in data[j]['authors']]
		npd[i, j] = distance(names1, names2)

# cluster with affinity propagation
ap = sklearn.cluster.AffinityPropagation().fit(npd)

# determine accuracy of labels
r = {}
for d, idx in zip(data, ap.labels_):
	m = re.search('^H(\d+)', d['pid'])
	hub = int(m.group(1))
	if hub not in r: r[hub] = {}
	if idx not in r[hub]: r[hub][idx] = 0
	r[hub][idx] += 1

def elsewhere(d, hid, idx):
	n = []
	for hub in d:
		if hub == hid: continue
		for i in d[hub]:
			if idx == i: n.append(hub)
	return n

gfound = 0
gmiss = 0
for hub in r:
	if arg.verbose: print('hub', hub, file=sys.stderr)
	found = 0
	miss = 0
	for idx in r[hub]:
		n = elsewhere(r, hub, idx)
		if len(n) == 0: found += r[hub][idx]
		else:           miss += len(n)
		if arg.verbose: print(f'\tc{idx}\t{r[hub][idx]}\t{n}', file=sys.stderr)
	if arg.verbose: print(found / (miss+found), file=sys.stderr)
	gfound += found
	gmiss += miss
print('global', gfound / (gfound + gmiss))

