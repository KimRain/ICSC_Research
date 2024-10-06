import argparse
import json
import math
import random

parser = argparse.ArgumentParser(description='fake co-publication data gen')
parser.add_argument('hubs', type=int, help='co-publication hubs')
parser.add_argument('--aph_min', type=int, default=5,
	help='minimum authors per hub [%(default)i]')
parser.add_argument('--aph_max', type=int, default=20,
	help='maximum authors per hub [%(default)i]')
parser.add_argument('--pph_min', type=int, default=10,
	help='minimum pubs per hub [%(default)i]')
parser.add_argument('--pph_max', type=int, default=50,
	help='maximum pubs per hub [%(default)i]')
parser.add_argument('--app_min', type=int, default=1,
	help='minimum authors per pub [%(default)i]')
parser.add_argument('--app_max', type=int, default=10,
	help='maximum authors per pub [%(default)i]')
parser.add_argument('--samename', type=float, default=0.1,
	help='probability of names crossing hubs [%(default).2f]')
parser.add_argument('--seed', type=int)
parser.add_argument('--verbose', action='store_true', help='show progress')
arg = parser.parse_args()

if arg.seed: random.seed(arg.seed)

# generate hubs with ids and unique names (actually also the id)
hubs = []
total_authors = 0
for hid in range(arg.hubs):
	authors = []
	for aid in range(int(random.randint(arg.aph_min, arg.aph_max))):
		authors.append({'id': f'H{hid}-A{aid}', 'name': f'H{hid}-A{aid}'})
		total_authors += 1
	hubs.append(authors)

# generate pairs of redundant author names across hubs
did = 0
for i in range(int(total_authors * arg.samename)):
	h1, h2 = random.sample(hubs, 2)
	a1 = random.choice(h1)
	a2 = random.choice(h2)
	if a1['name'].startswith('D') or a2['name'].startswith('D'): continue
	name = f'D{did}'
	a1['name'] = name
	a2['name'] = name
	did += 1

# generate pubs
pubs = []
pid = 0
for hid, hub in enumerate(hubs):
	npubs = random.randint(arg.pph_min, arg.pph_max)
	for _ in range(npubs):
		n = int(random.randint(arg.app_min, min([len(hub), arg.app_max])))
		pubs.append({'pid': f'H{hid}-P{pid}', 'authors': random.sample(hub, n)})
		pid += 1

print(json.dumps(pubs, indent=4))
