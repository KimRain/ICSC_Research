import argparse
import random
import string
import numpy as np
from sklearn.cluster import HDBSCAN
from collections import defaultdict
from itertools import combinations
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
matplotlib.use('Agg')

parser = argparse.ArgumentParser(description='fake co-publication data gen')
parser.add_argument('hubs', type=int, help='co-publication hubs')
parser.add_argument('--authorsperhub', type=int, default=10)
parser.add_argument('--pubsperhub', type=int, default=10)
parser.add_argument('--dupauthor', type=float, default=0.1)
parser.add_argument('--minauthor', type=int, default=2, help='min authors')
parser.add_argument('--maxauthor', type=int, default=9, help='max authors')
parser.add_argument('--nonhub', type=float, default=0.25,
                    help='non-hub pubs %(default)s')
parser.add_argument('--escape', type=float, default=0.10,
                    help='author crosses hubs %(default)s')
parser.add_argument('--seed', type=int, default=42)
parser.add_argument('--verbose', action='store_true', help='show progress')
arg = parser.parse_args()

if arg.seed: random.seed(arg.seed)

Authors = {}


def random_authors(n, f):
	my_authors = []
	for _ in range(n):
		name = ''.join(random.choice(string.ascii_uppercase) for _ in range(8))
		porcid = random.randint(1000000000, 9999999999)
		if random.random() > f or len(Authors) == 0:
			Authors[name] = 1
			my_authors.append((name, porcid))
		else:
			a = random.choice(list(Authors.keys()))
			Authors[a] += 1
			my_authors.append((a, porcid))
	return my_authors


def generate_pubs(n, f, mn, mx):
	authors = random_authors(n, f)
	pubs = []
	for i in range(n):
		this_pub = []
		auts = random.sample(authors, random.randint(mn, mx))
		for a in auts:
			this_pub.append(a)
		pubs.append(this_pub)
	return pubs


# if this doesn't work delete this fxn
# making hubs using distance matrix + clustering methods

def generate_hubs(publications):
	# co-authorship dict
	co_authors = defaultdict(set)
	unique_auts = defaultdict(set)

	for pub in publications:
		# counts num of time author appears
		for aut in pub:
			unique_auts[aut].add(tuple(pub))
		for aut1, aut2 in combinations(pub, 2):
			co_authors[aut1].add(aut2)
			co_authors[aut2].add(aut1)

	# calc pairwise similarity
	auts = list(co_authors.keys())
	similarity_matrix = np.zeros((len(auts), len(auts)))

	for i, aut1 in enumerate(auts):
		for j, aut2 in enumerate(auts):
			if i != j:
				# using Jaccard similarity
				intersection = len(co_authors[aut1].intersection((co_authors[aut2])))
				union = len(co_authors[aut1].union(co_authors[aut2]))
				if union > 0:
					similarity_matrix[i, j] = (intersection / union)

	# modify similarity matrix to account for authors with same name
	for i, aut1 in enumerate(auts):
		for j, aut2 in enumerate(auts):
			if aut1[0] == aut2[0] and i != j:
				if unique_auts[aut1] != unique_auts[aut2]:
					similarity_matrix[i,j] *= 0.001


	distance_matrix = 1 - similarity_matrix

# visualizing similarity matrix
	plt.figure(figsize=(30,15))
	sns.heatmap(similarity_matrix, annot=True, fmt=".2f", cmap='coolwarm', xticklabels=auts, yticklabels=auts)
	plt.title("Author Similarity Matrix")
	plt.xlabel("Authors")
	plt.ylabel("Authors")
	plt.savefig('similarity_matrix.png')  # Save the figure
	plt.close()

# time to cluster into hubs using DBSCAN
	hdbscan = HDBSCAN(min_cluster_size=2, metric='precomputed')
	labels = hdbscan.fit_predict(distance_matrix)

	hubs = defaultdict(list)
	for label, author in zip(labels, auts):
		if label != -1:
			hubs[label].append(author)

	return hubs


# store all data in a nested dict. structure
# labeled data
all_hubs = {}

# list of lists containing all authors/pub
# unlabeled data
all_pubs = []

""""# each publication should have a unique id like PMID
# that the authors are associated to
used_pmids = set()

# adding PMIDs makes too many hubs...
def generate_pmid(used_pmids):
	while True:
		pmid = random.randint(1, 10 ** 9)
		if pmid not in used_pmids:
			used_pmids.add(pmid)
			return pmid
"""

for i in range(arg.hubs):
	# assign hub_ids
	hub_id = i + 1
	hub_data = {}
	pubs = generate_pubs(arg.pubsperhub, arg.dupauthor, arg.minauthor, arg.maxauthor)
	for pub_id, pub in enumerate(pubs, start=1):
		hub_data[f'publication {pub_id}'] = \
			[{"author": author[0], "porcid": author[1]} for author in pub]
		all_hubs[f'hub_id:{hub_id}'] = hub_data

		# store just author names in list
		all_pubs.append(([author[0] for author in pub]))

# output data, might change to outputting JSON file later
# print statements for my visualization
print(Authors)

"""for hub_id, hub_data in all_hubs.items():
	print(f"{hub_id}:")
	for pub_id, authors in hub_data.items():
		print(f" {pub_id}: {authors}")
	print()"""

print(f'num of pubs:{len(all_pubs)}')
print("authors per pub:")
for i, pub_authors in enumerate(all_pubs, start=1):
	print(pub_authors)

hubs = generate_hubs(all_pubs)

for hub_id, authors in hubs.items():
	print(f"hub{hub_id}: {authors}")
