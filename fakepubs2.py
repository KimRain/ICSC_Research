import argparse
import csv
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
		name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
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
		for a in auts: this_pub.append(a)
		pubs.append(this_pub)
	return pubs

all_pubs = []
for i in range(arg.hubs):
	pubs = generate_pubs(arg.pubsperhub, arg.dupauthor, arg.minauthor,
		arg.maxauthor)
	for pub in pubs: all_pubs.append(pub)
print(all_pubs)

# The porcids are the answer, ideally in the list of authors we don't
# know whether the authors are unique individuals or the same person
# must compare somehow to identify if authors are different people
# then assign them a porcid

with open('authors_only.csv', 'w', newline='') as fpa, \
		open('porcids_only.csv', 'w', newline='') as fpp, \
		open('author_porcid.csv', 'w', newline='') as fpx, \
		open('author_edges.csv', 'w', newline='') as fnetwork, \
		open('edges_with_porcid.csv', 'w', newline='') as fedges_porcid:

	author_writer = csv.writer(fpa)
	porcid_writer = csv.writer(fpp)
	author_porcid_writer = csv.writer(fpx)
	network_writer = csv.writer(fnetwork)
	edges_porcid_writer = csv.writer(fedges_porcid)

	# Write headers
	author_writer.writerow(['Authors'])
	porcid_writer.writerow(['PORCIDs'])
	author_porcid_writer.writerow(['Author', 'PORCID'])
	network_writer.writerow(['Start Node', 'End Node'])  # Header for edges
	edges_porcid_writer.writerow(['Start Node', 'End Node', 'Last Author PORCID'])  # Header for edges with PORCID

	# Write data to CSV
	for pub in all_pubs:
		authors = [author for author, porcid in pub]
		porcids = [porcid for author, porcid in pub]

		author_writer.writerow([authors])  #All authors in one cell
		porcid_writer.writerow([porcids])  #All PORCIDs in one cell

		for author, porcid in pub:
			author_porcid_writer.writerow([author, porcid])

		last_author = pub[-1][0]
		last_author_porcid = pub[-1][1]  # Last author's PORCID
		last_author_node = f"{last_author}"  # Mark last author uniquely

		for idx, (author, _) in enumerate(pub[:-1]):  # All others as End Nodes
			author_node = f"{author}"
			network_writer.writerow([last_author_node, author_node])  # Normal edges
			edges_porcid_writer.writerow([last_author_node, author_node, last_author_porcid])  # Edges with PORCID

if arg.verbose: print(f"Generated {len(all_pubs)} publications.")
print(Authors)