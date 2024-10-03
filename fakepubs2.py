import argparse
import random
import string

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

# store all data in a nested dict. structure
# labeled data
all_hubs = {}

# list of lists containing all authors/pub
# unlabeled data
all_pubs = []

for i in range(arg.hubs):
	# assign hub_ids
	hub_id = i + 1
	hub_data = {}
	pubs = generate_pubs(arg.pubsperhub, arg.dupauthor, arg.minauthor, arg.maxauthor)
	for pub_id, pub in enumerate(pubs, start=1):
		hub_data[f'publication {pub_id}'] = [{"author": author[0], "porcid": author[1]} for author in pub]
		all_hubs[f'hub_id:{hub_id}'] = hub_data

		# store just author names in list
		all_pubs.append([author[0] for author in pub])

# output data, might change to outputting JSON file later
# print statements for my visualization
for hub_id, hub_data in all_hubs.items():
	print(f"{hub_id}:")
	for pub_id, authors in hub_data.items():
		print(f" {pub_id}: {authors}")
	print()

print(f'num of pubs:{len(all_pubs)}')
print("authors per pub:")
for i, pub_authors in enumerate(all_pubs, start=1):
	print(pub_authors)


