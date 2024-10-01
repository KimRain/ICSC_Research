import argparse
import math
import random

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
parser.add_argument('--seed', type=int)
parser.add_argument('--verbose', action='store_true', help='show progress')
arg = parser.parse_args()

if arg.seed: random.seed(arg.seed)

Authors = {}
Porcids = 0

def random_authors(n, f):
	global Porcids
	alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	my_authors = []
	for _ in range(n):
		name = []
		for _ in range(10): name.append(random.choice(alph))
		name = ''.join(name)
		porcid = Porcids
		Porcids += 1
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
		for a in auts: this_pub.append(a)
		pubs.append(this_pub)
	return pubs

all_pubs = []
for i in range(arg.hubs):
	pubs = generate_pubs(arg.pubsperhub, arg.dupauthor, arg.minauthor,
		arg.maxauthor)
	for pub in pubs: all_pubs.append(pub)

fpa = open('authors_only.txt', 'w')
fpp = open('porcids_only.txt', 'w')
fpx = open('author_porcid.txt', 'w')

for pub in pubs:
	authors = []
	porcids = []
	for author, porcid in pub:
		authors.append(author)
		porcids.append(porcid)
	fpa.write(f'{authors}\n')
	fpp.write(f'{porcids}\n')
	fpx.write(f'{pub}\n')
